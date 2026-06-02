#!/usr/bin/env python3
"""
extract_topology.py
===================
Parses the Spring PetClinic source tree and extracts:
  1. Program/module call graph (DI-resolved + annotation-routed)
  2. Data dependency graph (which modules touch which tables/stores)
  3. Entry points (HTTP routes from @GetMapping/@PostMapping + mvc-core-config.xml)
  4. Dead-end candidates (no inbound edges after entry-point resolution)

Writes:
  analysis/src/topology.json   — machine-readable graph
  prints human summary to stdout

Run from repo root:
    python analysis/src/extract_topology.py
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent.parent
SRC_MAIN_JAVA = REPO_ROOT / "src" / "main" / "java"
SRC_MAIN_WEBAPP = REPO_ROOT / "src" / "main" / "webapp"
SRC_MAIN_RESOURCES = REPO_ROOT / "src" / "main" / "resources"
OUT_JSON = Path(__file__).parent / "topology.json"

BASE_PKG = "org.springframework.samples.petclinic"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def short_name(fqcn: str) -> str:
    """Return the simple class name from a FQCN or file path fragment."""
    return fqcn.split(".")[-1].replace(".java", "")


def pkg_to_domain(fqcn: str) -> str:
    """Map a FQCN to one of our logical domains."""
    if ".web." in fqcn or fqcn.endswith("Controller") or fqcn.endswith("Formatter") or fqcn.endswith("Validator"):
        return "web"
    if ".service." in fqcn:
        return "service"
    if ".repository.jdbc" in fqcn:
        return "repo_jdbc"
    if ".repository.jpa" in fqcn:
        return "repo_jpa"
    if ".repository.springdatajpa" in fqcn:
        return "repo_springdata"
    if ".repository." in fqcn:
        return "repo_interface"
    if ".model." in fqcn:
        return "model"
    if ".util." in fqcn:
        return "util"
    if fqcn.endswith("PetclinicInitializer"):
        return "bootstrap"
    return "other"


def file_to_fqcn(path: Path) -> str:
    """Convert a .java path to a fully qualified class name."""
    rel = path.relative_to(SRC_MAIN_JAVA)
    return str(rel).replace("\\", ".").replace("/", ".").removesuffix(".java")


# ---------------------------------------------------------------------------
# Step 1: Collect all Java source files
# ---------------------------------------------------------------------------

def collect_java_files():
    return list(SRC_MAIN_JAVA.rglob("*.java"))


# ---------------------------------------------------------------------------
# Step 2: Parse each file for metadata
# ---------------------------------------------------------------------------

IMPORT_RE = re.compile(r'import\s+(org\.springframework\.samples\.petclinic\.[A-Za-z.]+)\s*;')
INJECT_RE = re.compile(r'(?:@Autowired|constructor|private\s+final)\s+.*?(\w+Repository|\w+Service|\w+Aspect|\w+Formatter)')
MAPPING_RE = re.compile(r'@(?:Get|Post|Put|Delete|Patch|Request)Mapping\s*\((?:[^)]*value\s*=\s*)?["\{]([^"\}]+)["\}]')
CLASS_RE   = re.compile(r'(?:public\s+)?(?:class|interface)\s+(\w+)')
ANNOTATION_RE = re.compile(r'@(Controller|Service|Repository|Component|RestController)')
TABLE_RE   = re.compile(r'FROM\s+(\w+)|JOIN\s+(\w+)|INSERT\s+INTO\s+(\w+)|UPDATE\s+(\w+)\s+SET|DELETE\s+FROM\s+(\w+)', re.IGNORECASE)
CACHEABLE_RE = re.compile(r'@Cacheable\s*\([^)]*value\s*=\s*"([^"]+)"')
FIELD_RE   = re.compile(r'private\s+(?:final\s+)?(\w+(?:Repository|Service))\s+(\w+)\s*;')
REQUEST_MAPPING_CLASS_RE = re.compile(r'@RequestMapping\s*\(\s*["\{]?([^"\}\)]+)["\}]?\s*\)')
JPA_QUERY_RE = re.compile(r'createQuery\s*\(\s*"([^"]+)"')
JDBC_SQL_RE  = re.compile(r'\.sql\s*\(\s*(?:"""([\s\S]*?)"""|"([^"]+)")')
NAMED_QUERY_RE = re.compile(r'@NamedQuery\s*\([^)]*query\s*=\s*"([^"]+)"')
VIEW_RETURN_RE = re.compile(r'return\s+"([^"]+)"')
REDIRECT_RE    = re.compile(r'return\s+"redirect:/([^"]+)"')


def parse_java_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    fqcn = file_to_fqcn(path)
    simple = short_name(fqcn)
    domain = pkg_to_domain(fqcn)

    # Imports of sibling classes → direct dependencies
    imports = [m.group(1) for m in IMPORT_RE.finditer(text)]

    # Injected field types (for DI resolution)
    injected_types = [(m.group(1), m.group(2)) for m in FIELD_RE.finditer(text)]

    # HTTP route annotations
    class_prefix = ""
    m = REQUEST_MAPPING_CLASS_RE.search(text)
    if m:
        class_prefix = m.group(1).strip().rstrip("/")
    routes = []
    for m in MAPPING_RE.finditer(text):
        verb = m.group(0).split("Mapping")[0].lstrip("@").upper()
        path_val = m.group(1).strip()
        full = (class_prefix + "/" + path_val).replace("//", "/")
        routes.append({"verb": verb, "path": full})

    # Spring stereotype
    stereotypes = [m.group(1) for m in ANNOTATION_RE.finditer(text)]

    # Tables accessed (SQL in JDBC repos and JPA JPQL)
    tables_read = set()
    tables_write = set()

    for m in JDBC_SQL_RE.finditer(text):
        sql = (m.group(1) or m.group(2) or "").upper()
        for tm in TABLE_RE.finditer(sql):
            groups = [g for g in tm.groups() if g]
            for tbl in groups:
                tbl = tbl.lower().strip()
                if tbl in ("set",): continue
                if "SELECT" in sql[:sql.find(tbl.upper())+20] or "FROM" in sql[:sql.find(tbl.upper())+20] or "JOIN" in sql[:sql.find(tbl.upper())+20]:
                    tables_read.add(tbl)
                elif "INSERT" in sql or "UPDATE" in sql or "DELETE" in sql:
                    tables_write.add(tbl)

    for m in JPA_QUERY_RE.finditer(text):
        sql = m.group(1).upper()
        for tm in TABLE_RE.finditer(sql):
            groups = [g for g in tm.groups() if g]
            for tbl in groups:
                tbl_l = tbl.lower().strip()
                if "SELECT" in sql or "FROM" in sql:
                    # JPQL uses entity names not table names; normalise
                    tables_read.add(tbl_l)
                else:
                    tables_write.add(tbl_l)

    # Cacheable annotation — cache store dependency
    cache_names = [m.group(1) for m in CACHEABLE_RE.finditer(text)]

    # View names returned
    views = []
    for m in VIEW_RETURN_RE.finditer(text):
        v = m.group(1)
        if not v.startswith("redirect:") and "/" in v:
            views.append(v)
    redirects = [m.group(1) for m in REDIRECT_RE.finditer(text)]

    return {
        "fqcn": fqcn,
        "simple": simple,
        "domain": domain,
        "stereotypes": stereotypes,
        "imports": imports,
        "injected_types": injected_types,
        "routes": routes,
        "tables_read": sorted(tables_read),
        "tables_write": sorted(tables_write),
        "cache_names": cache_names,
        "views": views,
        "redirects": redirects,
    }


# ---------------------------------------------------------------------------
# Step 3: Parse Spring XML config for DI wiring (bean → impl resolution)
# ---------------------------------------------------------------------------

COMPONENT_SCAN_RE = re.compile(r'<context:component-scan\s+base-package="([^"]+)"')
JPA_REPOS_RE      = re.compile(r'<jpa:repositories\s+base-package="([^"]+)"')
PROFILE_RE        = re.compile(r'<beans\s+profile="([^"]+)"')
MVC_CONTROLLER_RE = re.compile(r'<mvc:view-controller\s+path="([^"]+)"\s+view-name="([^"]+)"')
EXCEPTION_VIEW_RE = re.compile(r'<property name="defaultErrorView" value="([^"]+)"')


def parse_spring_xml(xml_path: Path) -> dict:
    text = xml_path.read_text(encoding="utf-8", errors="replace")
    return {
        "component_scans": COMPONENT_SCAN_RE.findall(text),
        "jpa_repos": JPA_REPOS_RE.findall(text),
        "profiles": PROFILE_RE.findall(text),
        "mvc_view_controllers": MVC_CONTROLLER_RE.findall(text),  # [(path, view_name)]
        "exception_views": EXCEPTION_VIEW_RE.findall(text),
        "file": str(xml_path.relative_to(REPO_ROOT)),
    }


# ---------------------------------------------------------------------------
# Step 4: Parse JSP + tag files for view dependencies
# ---------------------------------------------------------------------------

JSP_INCLUDE_RE = re.compile(r'<%@\s*include\s+file="([^"]+)"')
JSP_TAGLIB_RE  = re.compile(r'<%@\s*taglib\s+.*?uri="([^"]+)"')
JSP_TAG_USE_RE = re.compile(r'<pet:\w+|<spring:\w+|<c:\w+|<fmt:\w+')
TAG_INSERT_RE  = re.compile(r'<insertAttribute\s+name="([^"]+)"')


def parse_jsp_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    name = path.stem
    rel = str(path.relative_to(SRC_MAIN_WEBAPP))
    includes = JSP_INCLUDE_RE.findall(text)
    uses_layout = "layout" in text
    return {
        "name": name,
        "rel_path": rel,
        "domain": "view",
        "includes": includes,
        "uses_layout": uses_layout,
    }


# ---------------------------------------------------------------------------
# Step 5: Parse schema.sql for canonical table names
# ---------------------------------------------------------------------------

CREATE_TABLE_RE = re.compile(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', re.IGNORECASE)


def parse_schema(schema_path: Path) -> list[str]:
    text = schema_path.read_text(encoding="utf-8", errors="replace")
    return [m.group(1).lower() for m in CREATE_TABLE_RE.finditer(text)]


# ---------------------------------------------------------------------------
# Step 6: Parse PetclinicInitializer for entry-point profile default
# ---------------------------------------------------------------------------

PROFILE_CONST_RE = re.compile(r'SPRING_PROFILE\s*=\s*"([^"]+)"')
SERVLET_MAP_RE   = re.compile(r'addMapping\s*\(\s*"([^"]+)"\s*\)')


def parse_initializer(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    profiles = PROFILE_CONST_RE.findall(text)
    servlet_mappings = SERVLET_MAP_RE.findall(text)
    return {
        "default_profile": profiles[0] if profiles else "jpa",
        "servlet_mappings": servlet_mappings,
    }


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def build_topology():
    topo = {
        "modules": {},
        "call_edges": [],       # {from, to, type}
        "data_edges": [],       # {module, table, access}  access=read|write
        "entry_points": [],     # {path, verb, controller, handler}
        "dead_candidates": [],
        "views": {},
        "tables": [],
        "spring_config": [],
        "init_info": {},
    }

    # --- Collect tables from H2 schema (canonical) ---
    h2_schema = SRC_MAIN_RESOURCES / "db" / "h2" / "schema.sql"
    if h2_schema.exists():
        topo["tables"] = parse_schema(h2_schema)

    # --- Initializer ---
    init_path = SRC_MAIN_JAVA / "org/springframework/samples/petclinic/PetclinicInitializer.java"
    if init_path.exists():
        topo["init_info"] = parse_initializer(init_path)

    # --- Spring XML config ---
    for xml_path in (SRC_MAIN_RESOURCES / "spring").glob("*.xml"):
        cfg = parse_spring_xml(xml_path)
        topo["spring_config"].append(cfg)

    # --- Java source files ---
    java_files = collect_java_files()
    modules_by_simple = {}
    modules_by_fqcn = {}

    for f in java_files:
        info = parse_java_file(f)
        topo["modules"][info["fqcn"]] = info
        modules_by_simple[info["simple"]] = info["fqcn"]
        modules_by_fqcn[info["fqcn"]] = info

    # --- Build call edges from imports + DI injection ---
    # Rule: if A imports B (both in petclinic package), edge A→B
    for fqcn, info in modules_by_fqcn.items():
        for imp in info["imports"]:
            if imp in modules_by_fqcn:
                topo["call_edges"].append({
                    "from": info["simple"],
                    "to": short_name(imp),
                    "type": "import"
                })
        # DI-injected field types
        for (field_type, field_name) in info["injected_types"]:
            # Resolve to concrete class via simple name lookup
            if field_type in modules_by_simple:
                target_fqcn = modules_by_simple[field_type]
                topo["call_edges"].append({
                    "from": info["simple"],
                    "to": field_type,
                    "type": "di_injection"
                })

    # --- Deduplicate call edges ---
    seen_edges = set()
    deduped = []
    for e in topo["call_edges"]:
        key = (e["from"], e["to"], e["type"])
        if key not in seen_edges:
            seen_edges.add(key)
            deduped.append(e)
    topo["call_edges"] = deduped

    # --- Build data edges ---
    # Map entity/JPQL names → table names
    entity_to_table = {
        "owner": "owners",
        "owners": "owners",
        "pet": "pets",
        "pets": "pets",
        "visit": "visits",
        "visits": "visits",
        "vet": "vets",
        "vets": "vets",
        "specialty": "specialties",
        "specialties": "specialties",
        "pettype": "types",
        "types": "types",
        "type": "types",
        "vet_specialties": "vet_specialties",
    }

    for fqcn, info in modules_by_fqcn.items():
        for raw_tbl in info["tables_read"]:
            tbl = entity_to_table.get(raw_tbl, raw_tbl)
            if tbl in topo["tables"] or tbl in entity_to_table.values():
                topo["data_edges"].append({
                    "module": info["simple"],
                    "table": tbl,
                    "access": "read",
                    "domain": info["domain"]
                })
        for raw_tbl in info["tables_write"]:
            tbl = entity_to_table.get(raw_tbl, raw_tbl)
            if tbl in topo["tables"] or tbl in entity_to_table.values():
                topo["data_edges"].append({
                    "module": info["simple"],
                    "table": tbl,
                    "access": "write",
                    "domain": info["domain"]
                })
        # JPA impls and Spring Data repos access tables via ORM — derive from model classes they import
        if info["domain"] in ("repo_jpa", "repo_springdata", "repo_interface"):
            for imp in info["imports"]:
                entity_simple = short_name(imp).lower()
                if entity_simple in entity_to_table:
                    tbl = entity_to_table[entity_simple]
                    # Decide read vs write from method patterns in the class
                    imp_path = SRC_MAIN_JAVA / (imp.replace(".", "/") + ".java")
                    has_save = "save(" in imp_path.read_text(encoding="utf-8", errors="replace") \
                               if imp_path.exists() else False
                    topo["data_edges"].append({
                        "module": info["simple"],
                        "table": tbl,
                        "access": "read_write" if has_save else "read",
                        "domain": info["domain"]
                    })

        # Cache stores
        for cache in info["cache_names"]:
            topo["data_edges"].append({
                "module": info["simple"],
                "table": f"cache:{cache}",
                "access": "read_write",
                "domain": info["domain"]
            })

    # Deduplicate data edges
    seen_data = set()
    deduped_data = []
    for e in topo["data_edges"]:
        key = (e["module"], e["table"], e["access"])
        if key not in seen_data:
            seen_data.add(key)
            deduped_data.append(e)
    topo["data_edges"] = deduped_data

    # --- Entry points ---
    # HTTP routes from @*Mapping annotations
    for fqcn, info in modules_by_fqcn.items():
        for route in info["routes"]:
            topo["entry_points"].append({
                "type": "http",
                "path": route["path"],
                "verb": route["verb"],
                "controller": info["simple"],
                "domain": info["domain"]
            })

    # MVC view controllers from XML config
    for cfg in topo["spring_config"]:
        for (path_val, view_name) in cfg.get("mvc_view_controllers", []):
            topo["entry_points"].append({
                "type": "http_static",
                "path": path_val,
                "verb": "GET",
                "controller": "MvcViewConfig",
                "view": view_name,
                "domain": "bootstrap"
            })

    # DispatcherServlet mapping from Initializer
    topo["entry_points"].append({
        "type": "servlet_dispatcher",
        "path": topo["init_info"].get("servlet_mappings", ["/"]),
        "controller": "PetclinicInitializer",
        "domain": "bootstrap"
    })

    # --- JSP views ---
    for jsp in (SRC_MAIN_WEBAPP / "WEB-INF" / "jsp").rglob("*.jsp"):
        info = parse_jsp_file(jsp)
        topo["views"][info["name"]] = info
    for tag in (SRC_MAIN_WEBAPP / "WEB-INF" / "tags").glob("*.tag"):
        topo["views"]["tag:" + tag.stem] = {
            "name": "tag:" + tag.stem,
            "rel_path": str(tag.relative_to(SRC_MAIN_WEBAPP)),
            "domain": "view_tag"
        }

    # --- Dead-end candidates ---
    # Modules with no inbound call_edges that are NOT entry points or model classes
    all_targets = {e["to"] for e in topo["call_edges"]}
    all_sources = {e["from"] for e in topo["call_edges"]}
    entry_simples = {ep["controller"] for ep in topo["entry_points"]}
    di_targets = set()  # Spring DI targets are "called" by the container
    for fqcn, info in modules_by_fqcn.items():
        if any(s in info["stereotypes"] for s in ("Controller", "Service", "Repository", "Component", "RestController")):
            di_targets.add(info["simple"])

    for fqcn, info in modules_by_fqcn.items():
        simple = info["simple"]
        if simple in ("package-info",):
            continue
        if simple not in all_targets and simple not in entry_simples and simple not in di_targets:
            if info["domain"] not in ("model",):  # model classes reached via ORM
                topo["dead_candidates"].append({
                    "module": simple,
                    "domain": info["domain"],
                    "fqcn": fqcn,
                    "note": "No inbound call edge; not a Spring-managed bean"
                })

    return topo


# ---------------------------------------------------------------------------
# Human summary printer
# ---------------------------------------------------------------------------

def print_summary(topo):
    print("=" * 70)
    print("TOPOLOGY SUMMARY — Spring PetClinic")
    print("=" * 70)

    print(f"\n{'MODULES':=<70}")
    domain_counts = defaultdict(int)
    for info in topo["modules"].values():
        domain_counts[info["domain"]] += 1
    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain:<25} {count:>3} files")
    print(f"  {'TOTAL':<25} {sum(domain_counts.values()):>3} files")

    print(f"\n{'ENTRY POINTS (HTTP Routes)':=<70}")
    http_eps = [ep for ep in topo["entry_points"] if ep["type"] == "http"]
    for ep in sorted(http_eps, key=lambda x: x.get("path", "")):
        print(f"  {ep['verb']:<7} {ep['path']:<45} -> {ep['controller']}")
    static_eps = [ep for ep in topo["entry_points"] if ep["type"] == "http_static"]
    for ep in static_eps:
        print(f"  {'GET':<7} {ep['path']:<45} -> view:{ep.get('view','')}")

    print(f"\n{'CALL EDGES':=<70}")
    edge_by_type = defaultdict(list)
    for e in topo["call_edges"]:
        edge_by_type[e["type"]].append(e)
    for etype, edges in sorted(edge_by_type.items()):
        print(f"  {etype}: {len(edges)} edges")
        for e in edges[:8]:
            print(f"    {e['from']} → {e['to']}")
        if len(edges) > 8:
            print(f"    ... and {len(edges)-8} more")

    print(f"\n{'DATA EDGES (module → table, access)':=<70}")
    # Group by table
    table_access = defaultdict(list)
    for e in topo["data_edges"]:
        table_access[e["table"]].append((e["module"], e["access"]))
    for tbl in sorted(table_access.keys()):
        accessors = table_access[tbl]
        writers = [m for m, a in accessors if "write" in a]
        readers = [m for m, a in accessors if "read" in a]
        print(f"  {tbl:<25}  readers={len(readers)}  writers={len(writers)}")
        if writers:
            print(f"    WRITE: {', '.join(sorted(set(writers)))}")

    print(f"\n{'DEAD-END CANDIDATES':=<70}")
    if topo["dead_candidates"]:
        for dc in topo["dead_candidates"]:
            print(f"  {dc['module']:<40} ({dc['domain']})  {dc.get('note','')}")
    else:
        print("  None found.")

    print(f"\n{'VIEWS (JSP)':=<70}")
    jsp_views = {k: v for k, v in topo["views"].items() if not k.startswith("tag:")}
    tag_views  = {k: v for k, v in topo["views"].items() if k.startswith("tag:")}
    print(f"  JSP pages : {len(jsp_views)}")
    for name, v in sorted(jsp_views.items()):
        print(f"    {v['rel_path']}")
    print(f"  Tag files : {len(tag_views)}")

    print(f"\n{'DATABASE TABLES (from h2/schema.sql)':=<70}")
    print(f"  {', '.join(topo['tables'])}")

    print(f"\n{'ACTIVE PROFILE DEFAULT':=<70}")
    print(f"  {topo['init_info'].get('default_profile', 'unknown')} (from PetclinicInitializer)")

    print("\n" + "=" * 70)
    print(f"Output: {OUT_JSON}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    topo = build_topology()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(topo, indent=2, default=str), encoding="utf-8")
    print_summary(topo)
