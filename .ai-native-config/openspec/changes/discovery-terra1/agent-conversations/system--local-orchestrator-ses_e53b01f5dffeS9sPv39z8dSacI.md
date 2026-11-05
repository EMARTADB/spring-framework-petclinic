# discovery-terra1 — system/local-orchestrator (ses_e53b01f5dffeS9sPv39z8dSacI)

### 1. User — 2026-11-05T15:24:38.459Z

lanza discovery

---

### 2. Assistant — 2026-11-05T15:24:38.506Z

_(no output)_

---

### 3. User — 2026-11-05T15:25:31.216Z

hola

---

### 4. Assistant — 2026-11-05T15:25:31.248Z

_(no output)_

---

### 5. User — 2026-11-05T15:27:46.158Z

lanza discovery

---

### 6. Assistant — 2026-11-05T15:27:46.185Z

_(Step started)_

#### Reasoning

```
**Planning repository validation steps**
```

#### Tool: todowrite

```json
{
  "todos": [
    {
      "content": "Validate workspace and detect OpenSpec state",
      "status": "in_progress",
      "priority": "high"
    },
    {
      "content": "Clarify workflow intent",
      "status": "pending",
      "priority": "high"
    },
    {
      "content": "Run selected local workflow",
      "status": "pending",
      "priority": "high"
    }
  ]
}
```

```
[
  {
    "content": "Validate workspace and detect OpenSpec state",
    "status": "in_progress",
    "priority": "high"
  },
  {
    "content": "Clarify workflow intent",
    "status": "pending",
    "priority": "high"
  },
  {
    "content": "Run selected local workflow",
    "status": "pending",
    "priority": "high"
  }
]
```

_(Step finished: tool-calls)_

---

### 7. Assistant — 2026-11-05T15:27:54.781Z

_(Step started)_

#### Tool: bash

```json
{
  "command": "git -C ./spring-framework-petclinic branch --show-current",
  "workdir": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic"
}
```

```
first-commit

```

#### Tool: bash

```json
{
  "command": "openspec list --json",
  "workdir": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic"
}
```

```
{
  "changes": [],
  "root": {
    "path": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic",
    "source": "nearest"
  }
}

```

_(Step finished: tool-calls)_

---

### 8. Assistant — 2026-11-05T15:28:02.365Z

_(Step started)_

#### Tool: todowrite

```json
{
  "todos": [
    {
      "content": "Validate workspace and detect OpenSpec state",
      "status": "completed",
      "priority": "high"
    },
    {
      "content": "Clarify workflow intent",
      "status": "in_progress",
      "priority": "high"
    },
    {
      "content": "Run selected local workflow",
      "status": "pending",
      "priority": "high"
    }
  ]
}
```

```
[
  {
    "content": "Validate workspace and detect OpenSpec state",
    "status": "completed",
    "priority": "high"
  },
  {
    "content": "Clarify workflow intent",
    "status": "in_progress",
    "priority": "high"
  },
  {
    "content": "Run selected local workflow",
    "status": "pending",
    "priority": "high"
  }
]
```

_(Step finished: tool-calls)_

---

### 9. Assistant — 2026-11-05T15:28:09.268Z

_(Step started)_

#### Tool: question

```json
{
  "questions": [
    {
      "question": "You are on branch `first-commit`. What would you like to do?",
      "header": "Workflow",
      "options": [
        {
          "label": "Start a new change (Recommended)",
          "description": "Choose a workflow and bootstrap a local OpenSpec change."
        },
        {
          "label": "Abort",
          "description": "Stop without creating or changing anything."
        }
      ]
    }
  ]
}
```

```
User has answered your questions: "You are on branch `first-commit`. What would you like to do?"="Start a new change (Recommended)". You can now continue with the user's answers in mind.
```

_(Step finished: tool-calls)_

---

### 10. Assistant — 2026-11-05T15:28:22.447Z

_(Step started)_

#### Reasoning

```
**Evaluating absolute glob usage**
```

#### Tool: glob

```json
{
  "pattern": "*/workflow.yaml",
  "path": "/home/mduenasb/work-framework/ainative-framework/config/workflows"
}
```

```
/home/mduenasb/work-framework/ainative-framework/config/workflows/context-rewrite/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/init/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/rewrite/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/evolutive/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/test-DO/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/modernization/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/parity-test/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/discovery/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/project-effort-estimation/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/context-generator/workflow.yaml
/home/mduenasb/work-framework/ainative-framework/config/workflows/context-init-ainative/workflow.yaml
```

_(Step finished: tool-calls)_

---

### 11. Assistant — 2026-11-05T15:28:27.945Z

_(Step started)_

#### Tool: question

```json
{
  "questions": [
    {
      "question": "Choose the workflow to bootstrap. Based on your message, Discovery is recommended.",
      "header": "Workflow",
      "options": [
        {
          "label": "discovery (Recommended)",
          "description": "Assess the legacy application and extract discovery artifacts."
        },
        {
          "label": "modernization",
          "description": "Run the modernization pipeline."
        },
        {
          "label": "evolutive",
          "description": "Define and implement an incremental change."
        },
        {
          "label": "init",
          "description": "Initialize project context."
        },
        {
          "label": "rewrite",
          "description": "Run application rewrite workflow."
        },
        {
          "label": "Other workflow",
          "description": "Select a different available workflow by name."
        }
      ]
    }
  ]
}
```

```
User has answered your questions: "Choose the workflow to bootstrap. Based on your message, Discovery is recommended."="discovery (Recommended)". You can now continue with the user's answers in mind.
```

_(Step finished: tool-calls)_

---

### 12. Assistant — 2026-11-05T15:28:40.775Z

_(Step started)_

#### Tool: read

```json
{
  "filePath": "/home/mduenasb/work-framework/ainative-framework/config/workflows/discovery/workflow.yaml"
}
```

```
<path>/home/mduenasb/work-framework/ainative-framework/config/workflows/discovery/workflow.yaml</path>
<type>file</type>
<content>
1: # Discovery Pipeline Configuration — Automated Phase
2: # This file is the single source of truth for pipeline routing logic.
3: # Consumed by the deterministic orchestrator (FastAPI) at runtime.
4: #
5: # Artifact dependencies and produced artifacts are NOT listed here — they are defined
6: # exclusively in the openspec schema.yaml and resolved at runtime via `openspec status --json`.
7: 
8: pipeline:
9:   name: discovery
10:   full_name: "Discovery"
11:   description: "Project discovery pipeline (automated phase): Context Discovery workflow - Legacy system discovery assessment document → Legacy system topology and dependency map → Legacy code business rules → review discovery documents"
12:   schema: discovery
13:   change_name: "{param:change_name}"  # This field must be slugified to be used as directory & branch name
14:   parameters:
15:     - name: change_name
16:       type: string
17:       required: true
18:       description: "Name of the change to be implemented"
19:     - name: description
20:       type: constant
21:       value: "Legacy system discovery: assessment document, topology map, business rules and review of the discovery documents."
22:       description: "Change summary used by the pr-publisher as the PR/MR body"
23:   # Global cycle policy — overridden per transition when specified
24:   cycle_policy:
25:     max_retries: 3
26:     on_max_retries: user      # "user" | "abort" | <stage-id>
27: 
28:   # Status signal prefix emitted by subagents at the end of their output.
29:   # The orchestrator parses lines starting with this prefix to determine routing.
30:   step_status_prefix: "STEP_STATUS"
31: 
32:   stages:
33: 
34:     - id: start-wf
35:       agent: orchestrators/discovery
36:       prompt: ~
37:       session: ~
38:       optional: false
39:       on_success:
40:         goto: discovery-assessment
41:         command: discovery-assess
42:         prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/init-assess/input-prompt.md"
43:         session: stateless
44:       on_failure:
45:         goto: user
46: 
47:     - id: discovery-assessment
48:       agent: discovery/init-assess
49:       command: discovery-assess
50:       prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/init-assess/input-prompt.md"
51:       session: stateless
52:       optional: false
53:       on_success:
54:         goto: discovery-map
55:         command: discovery-map
56:         prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/init-map/input-prompt.md"
57:         session: stateless
58:       on_failure:
59:         goto: user
60: 
61:     - id: discovery-map
62:       agent: discovery/init-map
63:       command: discovery-map
64:       prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/init-map/input-prompt.md"
65:       session: stateless
66:       optional: false
67:       on_success:
68:         goto: business-rules-extractor
69:         command: discovery-extract-rules
70:         prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/init-business-rules/input-prompt.md"
71:         session: stateless
72:       on_failure:
73:         goto: user
74: 
75:     - id: business-rules-extractor
76:       agent: discovery/init-business-rules
77:       command: discovery-extract-rules
78:       prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/init-business-rules/input-prompt.md"
79:       session: stateless
80:       optional: false
81:       on_success:
82:         goto: discovery-functional
83:         command: discovery-extract-functional
84:         prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/init-functional/input-prompt.md"
85:         session: stateless
86:       on_failure:
87:         goto: user
88: 
89:     - id: discovery-functional
90:       agent: discovery/init-functional
91:       command: discovery-extract-functional
92:       prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/init-functional/input-prompt.md"
93:       session: stateless
94:       optional: false
95:       on_success:
96:         goto: review
97:         prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/reviewer/input-prompt.md"
98:         session: stateless
99:       on_failure:
100:         goto: user
101: 
102:     - id: review
103:       agent: discovery/reviewer
104:       prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/discovery/reviewer/input-prompt.md"
105:       session: stateless
106:       optional: false
107:       on_success:
108:         goto: pr-publish
109:         prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/pr-publisher/input-prompt.md"
110:         session: stateless
111:       on_failure:
112:         goto: user
113: 
114:     - id: pr-publish
115:       agent: pr-publisher
116:       prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/pr-publisher/input-prompt.md"
117:       session: stateless
118:       optional: false
119:       on_success:
120:         goto: archive
121:         prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/archivist/input-prompt.md"
122:         session: stateless
123:       on_failure:
124:         goto: user
125: 
126:     - id: archive
127:       agent: archivist
128:       prompt: "{env:AINATIVE_FRAMEWORK_DIR}/config/agents/archivist/input-prompt.md"
129:       session: stateless
130:       optional: false
131:       on_success:
132:         goto: done
133:       on_failure:
134:         goto: user
135: 
136:   # Escalation message templates — used when goto: user is triggered.
137:   # {stage}, {reason}, {retry_count}, {options} are interpolated by the orchestrator at runtime.
138:   escalation_messages:
139:     default: |
140:       The pipeline has reached a decision point that requires your input.
141: 
142:       Stage:        {stage}
143:       Reason:       {reason}
144:       Retry count:  {retry_count}
145: 
146:       Please choose how to proceed:
147:       {options}
148:     cycle_broken: |
149:       The pipeline has cycled {retry_count} times between {stage_a} and {stage_b} without resolution.
150: 
151:       Last known condition: {condition}
152: 
153:       Please choose how to proceed:
154:       {options}

(End of file - total 154 lines)
</content>
```

_(Step finished: tool-calls)_

---

### 13. Assistant — 2026-11-05T15:28:46.385Z

_(Step started)_

#### Reasoning

```
**Clarifying parameter naming requirement**
```

#### Tool: question

```json
{
  "questions": [
    {
      "question": "Provide a slugified name for this Discovery change (used for the OpenSpec directory and Git branch).",
      "header": "Change name",
      "options": [
        {
          "label": "Use `petclinic-discovery` (Recommended)",
          "description": "A descriptive valid name inferred from the project."
        }
      ]
    }
  ]
}
```

```
User has answered your questions: "Provide a slugified name for this Discovery change (used for the OpenSpec directory and Git branch)."="discovery-terra1". You can now continue with the user's answers in mind.
```

_(Step finished: tool-calls)_

---

### 14. Assistant — 2026-11-05T15:29:07.018Z

_(Step started)_

#### Reasoning

```
**Verifying parent existence before creating**
```

#### Tool: bash

```json
{
  "command": "ls ./openspec",
  "workdir": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic"
}
```

```
changes
config.yaml
schemas
specs

```

_(Step finished: tool-calls)_

---

### 15. Assistant — 2026-11-05T15:29:12.759Z

_(Step started)_

#### Tool: bash

```json
{
  "command": "openspec new change \"discovery-terra1\" --schema discovery && git -C ./spring-framework-petclinic switch \"openspec/changes/discovery-terra1\" 2>/dev/null || git -C ./spring-framework-petclinic switch -c \"openspec/changes/discovery-terra1\"",
  "workdir": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic"
}
```

```
- Creating change 'discovery-terra1' with schema 'discovery'...
Created change 'discovery-terra1' at openspec/changes/discovery-terra1/
Schema: discovery
Next: openspec status --change discovery-terra1
Switched to a new branch 'openspec/changes/discovery-terra1'

```

_(Step finished: tool-calls)_

---

### 16. Assistant — 2026-11-05T15:29:19.879Z

_(Step started)_

#### Reasoning

```
**Assessing log file creation constraints**
```

#### Tool: read

```json
{
  "filePath": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic/openspec/changes/discovery-terra1"
}
```

```
<path>/home/mduenasb/ainative-workspaces/spring-framework-petclinic/openspec/changes/discovery-terra1</path>
<type>directory</type>
<entries>
.openspec.yaml
agent-conversations/

(2 entries)
</entries>
```

_(Step finished: tool-calls)_

---

### 17. Assistant — 2026-11-05T15:29:30.474Z

_(Step started)_

#### Reasoning

```
**Planning metadata writing with manual check**
```

#### Tool: question

```json
{
  "questions": [
    {
      "question": "The first stage of this workflow (`start-wf`) uses an Agentic Orchestrator (`orchestrators/discovery`) that needs direct user interaction via its subagents. Due to an opencode limitation, descendant subagents cannot use the `question` tool. Would you like to run this stage manually in a separate terminal?",
      "header": "Manual AO",
      "options": [
        {
          "label": "Yes, run manually (Recommended)",
          "description": "Receive the exact orchestrator input and continue after it writes the session result."
        },
        {
          "label": "No, run automatically",
          "description": "Run it through the local pipeline; its interactive subagents may be blocked."
        }
      ]
    }
  ]
}
```

```
User has answered your questions: "The first stage of this workflow (`start-wf`) uses an Agentic Orchestrator (`orchestrators/discovery`) that needs direct user interaction via its subagents. Due to an opencode limitation, descendant subagents cannot use the `question` tool. Would you like to run this stage manually in a separate terminal?"="Yes, run manually (Recommended)". You can now continue with the user's answers in mind.
```

_(Step finished: tool-calls)_

---

### 18. Assistant — 2026-11-05T15:29:45.801Z

_(Step started)_

#### Tool: question

```json
{
  "questions": [
    {
      "question": "Do you want to stop after a specific workflow stage? The pipeline will pause after that stage and report its status.",
      "header": "Stop after",
      "options": [
        {
          "label": "No—run uninterrupted (Recommended)",
          "description": "Continue until completion or an escalation."
        },
        {
          "label": "start-wf",
          "description": "Pause after the orchestrator stage."
        },
        {
          "label": "discovery-assessment",
          "description": "Pause after the assessment."
        },
        {
          "label": "discovery-map",
          "description": "Pause after the topology map."
        },
        {
          "label": "business-rules-extractor",
          "description": "Pause after business-rules extraction."
        },
        {
          "label": "discovery-functional",
          "description": "Pause after functional discovery."
        },
        {
          "label": "review",
          "description": "Pause after review."
        },
        {
          "label": "pr-publish",
          "description": "Pause after publishing."
        },
        {
          "label": "archive",
          "description": "Pause after archival."
        }
      ]
    }
  ]
}
```

```
User has answered your questions: "Do you want to stop after a specific workflow stage? The pipeline will pause after that stage and report its status."="No—run uninterrupted (Recommended)". You can now continue with the user's answers in mind.
```

_(Step finished: tool-calls)_

---

### 19. Assistant — 2026-11-05T15:29:59.499Z

_(Step started)_

#### Reasoning

```
**Planning subagent creation for writing**
```

#### Tool: task

```json
{
  "description": "Create pipeline metadata",
  "subagent_type": "general",
  "prompt": "Write exactly this JSON content to `./openspec/changes/discovery-terra1/agent-sessions-log.json` in the current workspace, creating no other files and making no other changes:\n[\n  {\n    \"workflow\": \"config/workflows/discovery/workflow.yaml\",\n    \"global_parameters\": {\n      \"change_name\": \"discovery-terra1\",\n      \"description\": \"Legacy system discovery: assessment document, topology map, business rules and review of the discovery documents.\"\n    }\n  }\n]\nReturn a brief confirmation only."
}
```

```
<task id="ses_e53ab14d4ffeXu2ekugOHfuq4o" state="completed">
<task_result>
Created `openspec/changes/discovery-terra1/agent-sessions-log.json` with the requested JSON.
</task_result>
</task>
```

_(Step finished: tool-calls)_

---

### 20. Assistant — 2026-11-05T15:30:26.996Z

_(Step started)_

#### Reasoning

```
**Planning direct text handoff**
```

#### Tool: todowrite

```json
{
  "todos": [
    {
      "content": "Validate workspace and detect OpenSpec state",
      "status": "completed",
      "priority": "high"
    },
    {
      "content": "Clarify workflow intent",
      "status": "completed",
      "priority": "high"
    },
    {
      "content": "Run selected local workflow",
      "status": "in_progress",
      "priority": "high"
    }
  ]
}
```

```
[
  {
    "content": "Validate workspace and detect OpenSpec state",
    "status": "completed",
    "priority": "high"
  },
  {
    "content": "Clarify workflow intent",
    "status": "completed",
    "priority": "high"
  },
  {
    "content": "Run selected local workflow",
    "status": "in_progress",
    "priority": "high"
  }
]
```

_(Step finished: tool-calls)_

---

### 21. Assistant — 2026-11-05T15:30:36.663Z

_(Step started)_

=== MANUAL ORCHESTRATOR HANDOFF ===

Stage: start-wf  
Agent: orchestrators/discovery

Copy the exact text inside the fence below as the input message for the
orchestrator agent:

```
lanza discovery
```

After the orchestrator finishes, type "continue" as a new message in this
session. I will read the AO's result from the session log and continue
with the remaining automated stages.

_(Step finished: stop)_

---

### 22. User — 2026-11-05T15:34:40.512Z

continue

---

### 23. Assistant — 2026-11-05T15:34:40.539Z

_(Step started)_

#### Tool: read

```json
{
  "filePath": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic/openspec/changes/discovery-terra1/agent-sessions-log.json"
}
```

```
<path>/home/mduenasb/ainative-workspaces/spring-framework-petclinic/openspec/changes/discovery-terra1/agent-sessions-log.json</path>
<type>file</type>
<content>
1: [
2:   {
3:     "workflow": "config/workflows/discovery/workflow.yaml",
4:     "global_parameters": {
5:       "change_name": "discovery-terra1",
6:       "description": "Legacy system discovery: assessment document, topology map, business rules and review of the discovery documents."
7:     }
8:   },
9:   {
10:     "session_id": "ses_e53a8efd5ffedtQqWVa5rLeL5o",
11:     "stage": "start-wf",
12:     "session_title": "Lanza discovery",
13:     "agent_name": "orchestrators/discovery",
14:     "init_timestamp": "2026-11-05T15:32:29.369Z",
15:     "end_timestamp": "2026-11-05T15:32:43.084Z",
16:     "iteration_count": 1,
17:     "finish_reason": "stop",
18:     "status": "success",
19:     "condition": null,
20:     "reason": null,
21:     "message_id": "msg_1ac572f51001N3N0xw9X6LiFHh"
22:   }
23: ]

(End of file - total 23 lines)
</content>
```

_(Step finished: tool-calls)_

---

### 24. Assistant — 2026-11-05T15:34:47.822Z

_(Step started)_

#### Reasoning

```
**Setting temporary environment variables for task**
```

#### Tool: bash

```json
{
  "command": "export AINATIVE_STAGE_ID=discovery-assessment",
  "workdir": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic"
}
```

```
(no output)
```

#### Tool: bash

```json
{
  "command": "printenv AINATIVE_FRAMEWORK_DIR",
  "workdir": "/home/mduenasb/ainative-workspaces/spring-framework-petclinic"
}
```

```
/home/mduenasb/work-framework/ainative-framework

```

_(Step finished: tool-calls)_

---

### 25. Assistant — 2026-11-05T15:34:57.577Z

_(Step started)_

#### Tool: read

```json
{
  "filePath": "/home/mduenasb/work-framework/ainative-framework/config/agents/discovery/init-assess/input-prompt.md"
}
```

```
<path>/home/mduenasb/work-framework/ainative-framework/config/agents/discovery/init-assess/input-prompt.md</path>
<type>file</type>
<content>
1: Execute the discovery workflow for the following change.
2: 
3: **Change name** (<name>): {param:"change_name"}
4: **Scanning directory** (<scan_directory>): .
5: **Doc directory** (<doc_directory>):   ./openspec/changes/{param:"change_name"}/discovery/
6: 
7: Using the discovery assessment workflow, generate a brand new map for each repository in this workspace, plus another "common" one documenting how the repositories relate at system level.
8: 
9: Save each repository assessment under:
10: 
11: <doc_directory>/<repository-name>/assessment/
12: 
13: If more than one repository is found, save the common system-level assessment under:
14: 
15: <doc_directory>/common/assessment/
16: 
17: Accept all defaults and proceed to the next step without asking.

(End of file - total 17 lines)
</content>
```

_(Step finished: tool-calls)_

---

### 26. Assistant — 2026-11-05T15:35:02.101Z

_(Step started)_

#### Reasoning

```
**Requesting exact content argument**
```

#### Tool: format_command

```json
{
  "command_name": "discovery-assess",
  "arguments": "Execute the discovery workflow for the following change.\n\n**Change name** (<name>): {param:\"change_name\"}\n**Scanning directory** (<scan_directory>): .\n**Doc directory** (<doc_directory>):   ./openspec/changes/{param:\"change_name\"}/discovery/\n\nUsing the discovery assessment workflow, generate a brand new map for each repository in this workspace, plus another \"common\" one documenting how the repositories relate at system level.\n\nSave each repository assessment under:\n\n<doc_directory>/<repository-name>/assessment/\n\nIf more than one repository is found, save the common system-level assessment under:\n\n<doc_directory>/common/assessment/\n\nAccept all defaults and proceed to the next step without asking.\n"
}
```

```
## Invocation context

Execute the discovery workflow for the following change.

**Change name** (<name>): {param:"change_name"}
**Scanning directory** (<scan_directory>): .
**Doc directory** (<doc_directory>):   ./openspec/changes/{param:"change_name"}/discovery/

Using the discovery assessment workflow, generate a brand new map for each repository in this workspace, plus another "common" one documenting how the repositories relate at system level.

Save each repository assessment under:

<doc_directory>/<repository-name>/assessment/

If more than one repository is found, save the common system-level assessment under:

<doc_directory>/common/assessment/

Accept all defaults and proceed to the next step without asking.


---

**Mode select.** If the invocation context above starts with `--portfolio`,
run **Portfolio mode**. Otherwise run **Workspace mode**.

---

# Portfolio mode (`--portfolio <parent-dir>`)

Sweep every immediate subdirectory of the parent dir and produce a
heat-map a steering committee can use to sequence a multi-year program.

## Step P1 — Per-system metrics

For each subdirectory `<sys>`:

```bash
cloc --quiet --csv <parent>/<sys>          # LOC by language
lizard -s cyclomatic_complexity <parent>/<sys> 2>/dev/null | tail -1
```

If `cloc`/`lizard` are not installed, fall back to `scc <parent>/<sys>`
(LOC + complexity) or `find` + `wc -l` grouped by extension, and estimate
complexity by counting decision keywords per file. Note which tool you used.

Capture: total SLOC, dominant language, file count, mean & max
cyclomatic complexity (CCN). For dependency freshness, locate the
manifest (`package.json`, `pom.xml`, `*.csproj`, `requirements*.txt`,
copybook dir) and note its age / pinned-version count.

## Step P2 — COCOMO-II effort

Compute person-months per system using COCOMO-II basic:
`PM = 2.94 × (KSLOC)^1.10` (nominal scale factors). Show the formula and
inputs so the figure is defensible, not a guess.

## Step P3 — Documentation coverage

For each system, count source files with vs without a header comment
block, and list architecture docs present (`README`, `docs/`, ADRs).
Report coverage % and the top undocumented subsystems.

## Step P4 — Render the heat-map

Write `<doc_directory>/portfolio.html` (dark `#1e1e1e` bg, `#d4d4d4` text,
`#cc785c` accent, system-ui font, all CSS inline). One row per system;
columns: **System · Lang · KSLOC · Files · Mean CCN · Max CCN · Dep
Freshness · Doc Coverage % · COCOMO PM · Risk**. Color-grade the PM and
Risk cells (green→amber→red). Below the table, a 2-3 sentence
sequencing recommendation: which system first and why.

Then stop. Tell the user to open `<doc_directory>/portfolio.html`.

---

# Workspace mode

Treat `<scan_directory>` as the **Discovery workspace**.

The workspace contains one or more repositories as immediate child
directories. `<scan_directory>` itself is not a repository to assess.

A workspace may contain repositories implemented with any programming
language, runtime, technology stack, architectural style, or execution model.

Do not assume any particular:

- programming language
- technology stack
- architecture
- repository role
- runtime
- deployment model
- integration style
- application type

Derive these characteristics from source code, configuration, build files,
runtime definitions, deployment descriptors, documentation, and other
available evidence.

Examples in this command are illustrative only and must not be interpreted
as an exhaustive list of supported technologies or repository types.

---

## Step W1 — Identify repositories

Inspect the immediate child directories of `<scan_directory>` and identify
the repositories that belong to the Discovery workspace.

Use available repository and project evidence such as:

- `.git`
- build descriptors
- dependency manifests
- source directory structures
- runtime or deployment descriptors
- project configuration
- language-specific project files
- repository documentation

Examples of project markers include `pom.xml`, `build.gradle`,
`package.json`, `*.csproj`, `pyproject.toml`, `requirements*.txt`,
Makefiles, JCL structures, COBOL source trees, Pascal project files,
copybook collections, or equivalent stack-specific markers.

These examples are not exhaustive.

Do not treat generated directories, dependency caches, build outputs, IDE
metadata, or workspace-support directories as independent repositories.

Record the resolved repositories before continuing.

For each repository use:

```text
<repository> = <scan_directory>/<repository-name>
<repository_doc_directory> = <doc_directory>/<repository-name>/assessment
```

Perform the complete **Repository assessment** independently for every
resolved repository.

Do not merge repository-level metrics, technologies, dependencies,
complexity, technical debt, security findings, architecture evidence,
documentation gaps, or effort estimates while performing these assessments.

After all repository-level assessments are complete:

- if the workspace contains one repository, finish with the repository-level
  result;
- if the workspace contains more than one repository, perform the
  **Common system assessment**.

---

# Repository assessment

For each `<repository>`, perform a complete modernization assessment.

This is the discovery phase — the goal is a fact-grounded executive brief that
a VP of Engineering could take into a budget meeting.

Assess the repository according to the technology and execution model actually
present in it. Do not force concepts from one stack onto another.

Work in this order:

## Step 1 — Quantitative inventory

Run and show the output of:

```bash
scc <repository>
```

Then run:

```bash
scc --by-file -s complexity <repository> | head -25
```

to identify the highest-complexity files. Capture the COCOMO effort/cost
estimate `scc` provides.

If `scc` is not installed, fall back in order:

1. `cloc <repository>` for the LOC table, then compute COCOMO-II effort
   yourself: `PM = 2.94 × (KSLOC)^1.10` (nominal scale factors). Show the
   inputs.

2. If `cloc` is also missing, use `find` + `wc -l` grouped by extension
   for LOC, and estimate complexity using stack-appropriate decision/control
   constructs.

Do not assume C-family syntax when assessing other languages. Adapt complexity
signals to the repository's actual language and execution model.

For example:

- COBOL: `IF`, `EVALUATE`, `WHEN`, `PERFORM`
- C-family / Java / JavaScript: `if`, `for`, `while`, `case`, `catch`
- Pascal: `if`, `case`, `for`, `while`, `repeat`
- other languages: use equivalent control-flow constructs

Compute COCOMO from KSLOC as above when needed.

Note in the assessment which tool and method were used so the figures are
reproducible.

## Step 2 — Technology fingerprint

Identify, with file evidence:

- Languages, frameworks, platforms, and runtime versions in use
- Build system and dependency manifest locations
- Data stores and persistent data structures
- Integration points and external interfaces
- Runtime, deployment, scheduling, transaction, batch, messaging, or
  invocation mechanisms where applicable
- Test presence and approximate coverage signal

Adapt the investigation to the repository.

Potential evidence may include schemas, copybooks, record definitions,
database definitions, ORM mappings, message definitions, APIs, queues,
files, batch jobs, transaction definitions, screen definitions, generated
interfaces, configuration-driven integrations, or other stack-specific
mechanisms.

Do not require any of these mechanisms to exist.

## Step 3 — Parallel deep analysis

Spawn three subagents **in parallel**:

1. **legacy-analyst** —

   "Build a structural map of <repository>.

   Identify the 5-12 major functional or structural domains/components
   represented in the repository, which source files or artifacts belong
   to each, and how they depend on each other through control flow, shared
   data, invocation, configuration, runtime definitions, or other
   stack-specific mechanisms.

   Group optional or feature-gated subsystems under one umbrella where
   appropriate.

   Return a markdown table + a Mermaid `graph TD` of domain-level
   dependencies. Use `subgraph` to cluster and cap at ~40 edges.

   Cite repository-relative file paths.

   Flag dangling references such as defined-but-missing targets or apparently
   unused elements, while accounting for dynamic, configuration-driven,
   scheduled, transactional, generated, or externally invoked entry points."

2. **legacy-analyst** —

   "Identify technical debt in <repository>.

   Adapt the analysis to the repository's actual technology and execution
   model.

   Look for dead code, deprecated constructs or APIs, duplication, overly
   coupled modules, god objects/programs, missing error handling, hardcoded
   configuration, obsolete dependencies, difficult-to-maintain structures,
   and other stack-specific technical debt.

   Return the top 10 findings ranked by remediation value, each with
   file:line evidence where available."

3. **security-auditor** —

   "Scan <repository> for security vulnerabilities.

   Adapt the security assessment to the repository's technology, execution
   model, trust boundaries, and interfaces.

   Consider applicable risks such as injection, authentication weaknesses,
   authorization weaknesses, hardcoded secrets, vulnerable dependencies,
   unsafe data handling, missing input validation, insecure configuration,
   file or resource permissions, and other stack-specific vulnerabilities.

   Return findings in CWE-tagged table form with file:line evidence and
   severity."

Wait for all three. Synthesize their findings.

## Step 4 — Production runtime overlay (optional)

If production telemetry or runtime evidence is available — for example an
observability/APM MCP server, batch logs, transaction logs, scheduler output,
runtime exports, operational records, or equivalent stack-specific evidence —
gather relevant runtime measurements for the repository's key execution paths.

These may include jobs, transactions, programs, services, routes, messages,
batch processes, scheduled tasks, or other runtime units.

Where meaningful, gather p50/p95/p99 wall-clock values and use them to:

- Tag functional or structural domains from Step 3 with their production
  execution cost.
- Calculate **p99 variance** (`p99/p50`) where those metrics are meaningful.
- Flag high-variance execution paths as operational risks.

Include a small **Runtime Profile** table adapted to the repository's
execution model.

If no telemetry is available, skip this step and note the gap in the
assessment.

Do not fabricate runtime metrics.

## Step 5 — Documentation gap analysis

Compare what the repository actually does against what its README,
documentation, comments, schemas, configuration, operational definitions,
or other available documentation says.

List the top 5 undocumented behaviors, structures, dependencies, interfaces,
or subsystems that a new engineer would need explained.

## Step 6 — Write the repository assessment

Create:

```text
<repository_doc_directory>/ASSESSMENT.md
<repository_doc_directory>/ARCHITECTURE.mmd
```

Write `<repository_doc_directory>/ASSESSMENT.md` with these sections:

- **Executive Summary**
  - 3-4 sentences: what this repository is responsible for, how big it is,
    how risky it is, and the headline recommendation.

- **System Inventory**
  - quantitative inventory
  - technology fingerprint

- **Architecture-at-a-Glance**
  - structural/domain table
  - reference the architecture diagram

- **Production Runtime Profile**
  - runtime evidence from Step 4, or explicitly state that no telemetry was
    available

- **Technical Debt**
  - top 10 findings, ranked

- **Security Findings**
  - CWE-tagged findings where applicable

- **Documentation Gaps**
  - top 5

- **Effort Estimation**
  - COCOMO-derived person-months
  - ±range
  - key cost drivers
  - calculation method

- **Recommended Modernization Pattern**
  - one of: Rehost / Replatform / Refactor / Rearchitect / Rebuild / Replace
  - one-paragraph rationale based on repository evidence

Write `<repository_doc_directory>/ARCHITECTURE.mmd` containing the Mermaid
domain/component dependency diagram from the legacy-analyst.

Verify that both files exist before continuing to the next repository.

---

# Common system assessment

Run this section **only when more than one repository was identified in
`<scan_directory>`**.

The purpose of the common assessment is to discover and document what can only
be understood by considering multiple repositories together.

`common` must not be a concatenation or duplication of repository-level
assessments.

Repository-local findings must remain in their corresponding repository
artifacts.

Read all generated repository-level:

```text
<doc_directory>/<repository-name>/assessment/ASSESSMENT.md
<doc_directory>/<repository-name>/assessment/ARCHITECTURE.mmd
```

Use those artifacts as the starting point.

Inspect repository source, configuration, runtime definitions, contracts,
data definitions, deployment artifacts, or other evidence when necessary to
confirm relationships between repositories.

Do not assume that repositories are related merely because they exist in the
same workspace.

Do not assume predefined repository roles such as frontend, backend, batch,
database, shared library, service, or adapter.

Discover each repository's role from evidence.

## Step C1 — Repository landscape

For each repository, identify its responsibility and role within the overall
system based on evidence.

Describe the role using terminology appropriate to the system being analyzed.

Examples may include, but are not limited to:

- transaction processing
- user interaction
- batch processing
- shared business definitions
- data processing
- integration
- reporting
- persistence
- calculation
- orchestration
- runtime support

Do not force a repository into one of these categories.

Record:

- repository name
- discovered responsibility
- main technologies/platforms
- major inputs
- major outputs
- confirmed relationships to other repositories
- supporting evidence

## Step C2 — Cross-repository relationships

Identify confirmed relationships between repositories.

Relationships may be expressed through any technology or execution mechanism.

Look for evidence including, but not limited to:

- program or module invocation
- procedure or routine calls
- APIs, RPC, service calls, or remote invocations
- batch or job invocation
- scheduler relationships
- transaction definitions
- message producers and consumers
- shared files
- exchanged files or generated outputs
- shared record layouts
- copybooks
- shared schemas
- contracts or interface definitions
- shared libraries
- imported modules
- shared or coordinated data stores
- database relationships
- configuration-driven references
- runtime or deployment relationships
- generated clients or generated interfaces
- user-interface to processing relationships
- external-system mediation
- other stack-specific integration mechanisms

These examples are not exhaustive.

For every confirmed relationship, identify:

- source repository
- target repository
- relationship or interaction type
- relevant artifact/program/module/interface
- direction
- supporting evidence
- confidence level

Distinguish clearly between:

- confirmed relationships
- inferred relationships
- unresolved potential relationships

Do not present inferred relationships as facts.

## Step C3 — System-level architecture

Build an end-to-end architecture view showing how the repositories form the
overall system.

Generate a Mermaid diagram showing:

- repository boundaries
- each repository's discovered responsibility
- confirmed relationships between repositories
- important shared resources or external systems where necessary to explain
  repository interaction

Do not reproduce complete internal repository-level call graphs.

Expand internal repository elements only where necessary to explain a
cross-repository relationship or critical end-to-end execution path.

## Step C4 — Cross-repository execution and data flows

Identify important flows that cross repository boundaries.

A flow may involve any combination of:

- user interaction
- program execution
- jobs
- transactions
- messages
- files
- databases
- services
- APIs
- shared data structures
- configuration
- schedulers
- external systems
- other stack-specific mechanisms

For each significant confirmed flow, describe:

- trigger
- participating repositories
- sequence of interactions
- data or control exchanged
- final outcome
- source evidence

Where the available evidence does not support a complete end-to-end flow,
document the gap instead of inventing missing steps.

## Step C5 — Shared and cross-repository concerns

Identify findings that can only be understood by considering multiple
repositories together.

Examples may include:

- duplicated or inconsistent contracts
- duplicated business concepts or data definitions
- incompatible interface assumptions
- shared data ownership
- coupling through shared files or databases
- version compatibility dependencies
- deployment or runtime coupling
- sequencing dependencies
- shared security assumptions
- cross-repository technical debt
- duplicated functionality
- conflicting data representations
- undocumented integration points
- modernization ordering constraints

These examples are not exhaustive.

Do not move repository-local findings into `common`.

## Step C6 — System-level modernization implications

Determine how relationships between repositories affect modernization.

Identify:

- repositories that can be modernized independently
- repositories that must be coordinated
- dependency ordering constraints
- contracts or data structures that must remain compatible
- shared runtime or deployment constraints
- cross-repository migration risks
- opportunities to decouple repositories before or during modernization

Base recommendations on evidence from the discovered system.

Do not assume that repositories should be merged, split, converted to
services, or migrated independently.

## Step C7 — Write the common assessment

Create:

```text
<doc_directory>/common/assessment/ASSESSMENT.md
<doc_directory>/common/assessment/ARCHITECTURE.mmd
```

Write `<doc_directory>/common/ASSESSMENT.md` with:

- **System Executive Summary**
  - what the repositories collectively represent
  - major relationships
  - headline system-level risks
  - headline modernization implication

- **Repository Landscape**
  - repository
  - discovered responsibility
  - technology/platform
  - main inputs/outputs
  - relationships

- **Cross-Repository Relationships**
  - confirmed relationships
  - evidence
  - confidence

- **Cross-Repository Execution and Data Flows**
  - significant end-to-end flows

- **System Architecture-at-a-Glance**
  - reference the common architecture diagram

- **Shared and Cross-Repository Risks**
  - findings that cannot be attributed to only one repository

- **System Documentation Gaps**
  - missing or ambiguous cross-repository knowledge

- **Modernization Dependencies and Sequencing**
  - dependencies that influence migration planning
  - coordination requirements
  - ordering constraints

- **Overall Modernization Pattern**
  - system-level recommendation
  - explicitly distinguish it from individual repository recommendations
    where they differ

For effort estimation, preserve each repository's independently calculated
COCOMO estimate.

If an overall figure is presented, show the repository estimates separately
and clearly explain how the overall value was derived.

Do not calculate system effort by treating the repositories as an artificially
merged source tree.

Write `<doc_directory>/common/assessment/ARCHITECTURE.mmd` containing the system-level
Mermaid diagram showing repository boundaries and confirmed relationships.

Verify both common artifacts exist.

---

# Present

Report:

- repositories discovered under `<scan_directory>`
- repository-level assessment artifacts generated for each repository
- whether a common system assessment was required
- common artifacts generated, when applicable
- unresolved or inferred cross-repository relationships, when applicable

For each repository suggest:

```text
glow -p <doc_directory>/<repository-name>/assessment/ASSESSMENT.md
```

If more than one repository exists, also suggest:

```text
glow -p <doc_directory>/common/assessment/ASSESSMENT.md
```
```

_(Step finished: tool-calls)_

---

### 27. Assistant — 2026-11-05T15:35:12.352Z

_(Step started)_

#### Reasoning

```
**Finalizing task with direct input**
```

#### Tool: task

_Status: running_

```json
{
  "description": "Run discovery assessment",
  "subagent_type": "discovery/init-assess",
  "command": "discovery-assess",
  "prompt": "## Invocation context\n\nExecute the discovery workflow for the following change.\n\n**Change name** (<name>): {param:\"change_name\"}\n**Scanning directory** (<scan_directory>): .\n**Doc directory** (<doc_directory>):   ./openspec/changes/{param:\"change_name\"}/discovery/\n\nUsing the discovery assessment workflow, generate a brand new map for each repository in this workspace, plus another \"common\" one documenting how the repositories relate at system level.\n\nSave each repository assessment under:\n\n<doc_directory>/<repository-name>/assessment/\n\nIf more than one repository is found, save the common system-level assessment under:\n\n<doc_directory>/common/assessment/\n\nAccept all defaults and proceed to the next step without asking.\n\n\n---\n\n**Mode select.** If the invocation context above starts with `--portfolio`,\nrun **Portfolio mode**. Otherwise run **Workspace mode**.\n\n---\n\n# Portfolio mode (`--portfolio <parent-dir>`)\n\nSweep every immediate subdirectory of the parent dir and produce a\nheat-map a steering committee can use to sequence a multi-year program.\n\n## Step P1 — Per-system metrics\n\nFor each subdirectory `<sys>`:\n\n```bash\ncloc --quiet --csv <parent>/<sys>          # LOC by language\nlizard -s cyclomatic_complexity <parent>/<sys> 2>/dev/null | tail -1\n```\n\nIf `cloc`/`lizard` are not installed, fall back to `scc <parent>/<sys>`\n(LOC + complexity) or `find` + `wc -l` grouped by extension, and estimate\ncomplexity by counting decision keywords per file. Note which tool you used.\n\nCapture: total SLOC, dominant language, file count, mean & max\ncyclomatic complexity (CCN). For dependency freshness, locate the\nmanifest (`package.json`, `pom.xml`, `*.csproj`, `requirements*.txt`,\ncopybook dir) and note its age / pinned-version count.\n\n## Step P2 — COCOMO-II effort\n\nCompute person-months per system using COCOMO-II basic:\n`PM = 2.94 × (KSLOC)^1.10` (nominal scale factors). Show the formula and\ninputs so the figure is defensible, not a guess.\n\n## Step P3 — Documentation coverage\n\nFor each system, count source files with vs without a header comment\nblock, and list architecture docs present (`README`, `docs/`, ADRs).\nReport coverage % and the top undocumented subsystems.\n\n## Step P4 — Render the heat-map\n\nWrite `<doc_directory>/portfolio.html` (dark `#1e1e1e` bg, `#d4d4d4` text,\n`#cc785c` accent, system-ui font, all CSS inline). One row per system;\ncolumns: **System · Lang · KSLOC · Files · Mean CCN · Max CCN · Dep\nFreshness · Doc Coverage % · COCOMO PM · Risk**. Color-grade the PM and\nRisk cells (green→amber→red). Below the table, a 2-3 sentence\nsequencing recommendation: which system first and why.\n\nThen stop. Tell the user to open `<doc_directory>/portfolio.html`.\n\n---\n\n# Workspace mode\n\nTreat `<scan_directory>` as the **Discovery workspace**.\n\nThe workspace contains one or more repositories as immediate child\ndirectories. `<scan_directory>` itself is not a repository to assess.\n\nA workspace may contain repositories implemented with any programming\nlanguage, runtime, technology stack, architectural style, or execution model.\n\nDo not assume any particular:\n\n- programming language\n- technology stack\n- architecture\n- repository role\n- runtime\n- deployment model\n- integration style\n- application type\n\nDerive these characteristics from source code, configuration, build files,\nruntime definitions, deployment descriptors, documentation, and other\navailable evidence.\n\nExamples in this command are illustrative only and must not be interpreted\nas an exhaustive list of supported technologies or repository types.\n\n---\n\n## Step W1 — Identify repositories\n\nInspect the immediate child directories of `<scan_directory>` and identify\nthe repositories that belong to the Discovery workspace.\n\nUse available repository and project evidence such as:\n\n- `.git`\n- build descriptors\n- dependency manifests\n- source directory structures\n- runtime or deployment descriptors\n- project configuration\n- language-specific project files\n- repository documentation\n\nExamples of project markers include `pom.xml`, `build.gradle`,\n`package.json`, `*.csproj`, `pyproject.toml`, `requirements*.txt`,\nMakefiles, JCL structures, COBOL source trees, Pascal project files,\ncopybook collections, or equivalent stack-specific markers.\n\nThese examples are not exhaustive.\n\nDo not treat generated directories, dependency caches, build outputs, IDE\nmetadata, or workspace-support directories as independent repositories.\n\nRecord the resolved repositories before continuing.\n\nFor each repository use:\n\n```text\n<repository> = <scan_directory>/<repository-name>\n<repository_doc_directory> = <doc_directory>/<repository-name>/assessment\n```\n\nPerform the complete **Repository assessment** independently for every\nresolved repository.\n\nDo not merge repository-level metrics, technologies, dependencies,\ncomplexity, technical debt, security findings, architecture evidence,\ndocumentation gaps, or effort estimates while performing these assessments.\n\nAfter all repository-level assessments are complete:\n\n- if the workspace contains one repository, finish with the repository-level\n  result;\n- if the workspace contains more than one repository, perform the\n  **Common system assessment**.\n\n---\n\n# Repository assessment\n\nFor each `<repository>`, perform a complete modernization assessment.\n\nThis is the discovery phase — the goal is a fact-grounded executive brief that\na VP of Engineering could take into a budget meeting.\n\nAssess the repository according to the technology and execution model actually\npresent in it. Do not force concepts from one stack onto another.\n\nWork in this order:\n\n## Step 1 — Quantitative inventory\n\nRun and show the output of:\n\n```bash\nscc <repository>\n```\n\nThen run:\n\n```bash\nscc --by-file -s complexity <repository> | head -25\n```\n\nto identify the highest-complexity files. Capture the COCOMO effort/cost\nestimate `scc` provides.\n\nIf `scc` is not installed, fall back in order:\n\n1. `cloc <repository>` for the LOC table, then compute COCOMO-II effort\nyourself: `PM = 2.94 × (KSLOC)^1.10` (nominal scale factors). Show the\ninputs.\n\n2. If `cloc` is also missing, use `find` + `wc -l` grouped by extension\nfor LOC, and estimate complexity using stack-appropriate decision/control\nconstructs.\n\nDo not assume C-family syntax when assessing other languages. Adapt complexity\nsignals to the repository's actual language and execution model.\n\nFor example:\n\n- COBOL: `IF`, `EVALUATE`, `WHEN`, `PERFORM`\n- C-family / Java / JavaScript: `if`, `for`, `while`, `case`, `catch`\n- Pascal: `if`, `case`, `for`, `while`, `repeat`\n- other languages: use equivalent control-flow constructs\n\nCompute COCOMO from KSLOC as above when needed.\n\nNote in the assessment which tool and method were used so the figures are\nreproducible.\n\n## Step 2 — Technology fingerprint\n\nIdentify, with file evidence:\n\n- Languages, frameworks, platforms, and runtime versions in use\n- Build system and dependency manifest locations\n- Data stores and persistent data structures\n- Integration points and external interfaces\n- Runtime, deployment, scheduling, transaction, batch, messaging, or\n  invocation mechanisms where applicable\n- Test presence and approximate coverage signal\n\nAdapt the investigation to the repository.\n\nPotential evidence may include schemas, copybooks, record definitions,\ndatabase definitions, ORM mappings, message definitions, APIs, queues,\nfiles, batch jobs, transaction definitions, screen definitions, generated\ninterfaces, configuration-driven integrations, or other stack-specific\nmechanisms.\n\nDo not require any of these mechanisms to exist.\n\n## Step 3 — Parallel deep analysis\n\nSpawn three subagents **in parallel**:\n\n1. **legacy-analyst** —\n\n   \"Build a structural map of <repository>.\n\n   Identify the 5-12 major functional or structural domains/components\n   represented in the repository, which source files or artifacts belong\n   to each, and how they depend on each other through control flow, shared\n   data, invocation, configuration, runtime definitions, or other\n   stack-specific mechanisms.\n\n   Group optional or feature-gated subsystems under one umbrella where\n   appropriate.\n\n   Return a markdown table + a Mermaid `graph TD` of domain-level\n   dependencies. Use `subgraph` to cluster and cap at ~40 edges.\n\n   Cite repository-relative file paths.\n\n   Flag dangling references such as defined-but-missing targets or apparently\n   unused elements, while accounting for dynamic, configuration-driven,\n   scheduled, transactional, generated, or externally invoked entry points.\"\n\n2. **legacy-analyst** —\n\n   \"Identify technical debt in <repository>.\n\n   Adapt the analysis to the repository's actual technology and execution\n   model.\n\n   Look for dead code, deprecated constructs or APIs, duplication, overly\n   coupled modules, god objects/programs, missing error handling, hardcoded\n   configuration, obsolete dependencies, difficult-to-maintain structures,\n   and other stack-specific technical debt.\n\n   Return the top 10 findings ranked by remediation value, each with\n   file:line evidence where available.\"\n\n3. **security-auditor** —\n\n   \"Scan <repository> for security vulnerabilities.\n\n   Adapt the security assessment to the repository's technology, execution\n   model, trust boundaries, and interfaces.\n\n   Consider applicable risks such as injection, authentication weaknesses,\n   authorization weaknesses, hardcoded secrets, vulnerable dependencies,\n   unsafe data handling, missing input validation, insecure configuration,\n   file or resource permissions, and other stack-specific vulnerabilities.\n\n   Return findings in CWE-tagged table form with file:line evidence and\n   severity.\"\n\nWait for all three. Synthesize their findings.\n\n## Step 4 — Production runtime overlay (optional)\n\nIf production telemetry or runtime evidence is available — for example an\nobservability/APM MCP server, batch logs, transaction logs, scheduler output,\nruntime exports, operational records, or equivalent stack-specific evidence —\ngather relevant runtime measurements for the repository's key execution paths.\n\nThese may include jobs, transactions, programs, services, routes, messages,\nbatch processes, scheduled tasks, or other runtime units.\n\nWhere meaningful, gather p50/p95/p99 wall-clock values and use them to:\n\n- Tag functional or structural domains from Step 3 with their production\n  execution cost.\n- Calculate **p99 variance** (`p99/p50`) where those metrics are meaningful.\n- Flag high-variance execution paths as operational risks.\n\nInclude a small **Runtime Profile** table adapted to the repository's\nexecution model.\n\nIf no telemetry is available, skip this step and note the gap in the\nassessment.\n\nDo not fabricate runtime metrics.\n\n## Step 5 — Documentation gap analysis\n\nCompare what the repository actually does against what its README,\ndocumentation, comments, schemas, configuration, operational definitions,\nor other available documentation says.\n\nList the top 5 undocumented behaviors, structures, dependencies, interfaces,\nor subsystems that a new engineer would need explained.\n\n## Step 6 — Write the repository assessment\n\nCreate:\n\n```text\n<repository_doc_directory>/ASSESSMENT.md\n<repository_doc_directory>/ARCHITECTURE.mmd\n```\n\nWrite `<repository_doc_directory>/ASSESSMENT.md` with these sections:\n\n- **Executive Summary**\n  - 3-4 sentences: what this repository is responsible for, how big it is,\n    how risky it is, and the headline recommendation.\n\n- **System Inventory**\n  - quantitative inventory\n  - technology fingerprint\n\n- **Architecture-at-a-Glance**\n  - structural/domain table\n  - reference the architecture diagram\n\n- **Production Runtime Profile**\n  - runtime evidence from Step 4, or explicitly state that no telemetry was\n    available\n\n- **Technical Debt**\n  - top 10 findings, ranked\n\n- **Security Findings**\n  - CWE-tagged findings where applicable\n\n- **Documentation Gaps**\n  - top 5\n\n- **Effort Estimation**\n  - COCOMO-derived person-months\n  - ±range\n  - key cost drivers\n  - calculation method\n\n- **Recommended Modernization Pattern**\n  - one of: Rehost / Replatform / Refactor / Rearchitect / Rebuild / Replace\n  - one-paragraph rationale based on repository evidence\n\nWrite `<repository_doc_directory>/ARCHITECTURE.mmd` containing the Mermaid\ndomain/component dependency diagram from the legacy-analyst.\n\nVerify that both files exist before continuing to the next repository.\n\n---\n\n# Common system assessment\n\nRun this section **only when more than one repository was identified in\n`<scan_directory>`**.\n\nThe purpose of the common assessment is to discover and document what can only\nbe understood by considering multiple repositories together.\n\n`common` must not be a concatenation or duplication of repository-level\nassessments.\n\nRepository-local findings must remain in their corresponding repository\nartifacts.\n\nRead all generated repository-level:\n\n```text\n<doc_directory>/<repository-name>/assessment/ASSESSMENT.md\n<doc_directory>/<repository-name>/assessment/ARCHITECTURE.mmd\n```\n\nUse those artifacts as the starting point.\n\nInspect repository source, configuration, runtime definitions, contracts,\ndata definitions, deployment artifacts, or other evidence when necessary to\nconfirm relationships between repositories.\n\nDo not assume that repositories are related merely because they exist in the\nsame workspace.\n\nDo not assume predefined repository roles such as frontend, backend, batch,\ndatabase, shared library, service, or adapter.\n\nDiscover each repository's role from evidence.\n\n## Step C1 — Repository landscape\n\nFor each repository, identify its responsibility and role within the overall\nsystem based on evidence.\n\nDescribe the role using terminology appropriate to the system being analyzed.\n\nExamples may include, but are not limited to:\n\n- transaction processing\n- user interaction\n- batch processing\n- shared business definitions\n- data processing\n- integration\n- reporting\n- persistence\n- calculation\n- orchestration\n- runtime support\n\nDo not force a repository into one of these categories.\n\nRecord:\n\n- repository name\n- discovered responsibility\n- main technologies/platforms\n- major inputs\n- major outputs\n- confirmed relationships to other repositories\n- supporting evidence\n\n## Step C2 — Cross-repository relationships\n\nIdentify confirmed relationships between repositories.\n\nRelationships may be expressed through any technology or execution mechanism.\n\nLook for evidence including, but not limited to:\n\n- program or module invocation\n- procedure or routine calls\n- APIs, RPC, service calls, or remote invocations\n- batch or job invocation\n- scheduler relationships\n- transaction definitions\n- message producers and consumers\n- shared files\n- exchanged files or generated outputs\n- shared record layouts\n- copybooks\n- shared schemas\n- contracts or interface definitions\n- shared libraries\n- imported modules\n- shared or coordinated data stores\n- database relationships\n- configuration-driven references\n- runtime or deployment relationships\n- generated clients or generated interfaces\n- user-interface to processing relationships\n- external-system mediation\n- other stack-specific integration mechanisms\n\nThese examples are not exhaustive.\n\nFor every confirmed relationship, identify:\n\n- source repository\n- target repository\n- relationship or interaction type\n- relevant artifact/program/module/interface\n- direction\n- supporting evidence\n- confidence level\n\nDistinguish clearly between:\n\n- confirmed relationships\n- inferred relationships\n- unresolved potential relationships\n\nDo not present inferred relationships as facts.\n\n## Step C3 — System-level architecture\n\nBuild an end-to-end architecture view showing how the repositories form the\noverall system.\n\nGenerate a Mermaid diagram showing:\n\n- repository boundaries\n- each repository's discovered responsibility\n- confirmed relationships between repositories\n- important shared resources or external systems where necessary to explain\n  repository interaction\n\nDo not reproduce complete internal repository-level call graphs.\n\nExpand internal repository elements only where necessary to explain a\ncross-repository relationship or critical end-to-end execution path.\n\n## Step C4 — Cross-repository execution and data flows\n\nIdentify important flows that cross repository boundaries.\n\nA flow may involve any combination of:\n\n- user interaction\n- program execution\n- jobs\n- transactions\n- messages\n- files\n- databases\n- services\n- APIs\n- shared data structures\n- configuration\n- schedulers\n- external systems\n- other stack-specific mechanisms\n\nFor each significant confirmed flow, describe:\n\n- trigger\n- participating repositories\n- sequence of interactions\n- data or control exchanged\n- final outcome\n- source evidence\n\nWhere the available evidence does not support a complete end-to-end flow,\ndocument the gap instead of inventing missing steps.\n\n## Step C5 — Shared and cross-repository concerns\n\nIdentify findings that can only be understood by considering multiple\nrepositories together.\n\nExamples may include:\n\n- duplicated or inconsistent contracts\n- duplicated business concepts or data definitions\n- incompatible interface assumptions\n- shared data ownership\n- coupling through shared files or databases\n- version compatibility dependencies\n- deployment or runtime coupling\n- sequencing dependencies\n- shared security assumptions\n- cross-repository technical debt\n- duplicated functionality\n- conflicting data representations\n- undocumented integration points\n- modernization ordering constraints\n\nThese examples are not exhaustive.\n\nDo not move repository-local findings into `common`.\n\n## Step C6 — System-level modernization implications\n\nDetermine how relationships between repositories affect modernization.\n\nIdentify:\n\n- repositories that can be modernized independently\n- repositories that must be coordinated\n- dependency ordering constraints\n- contracts or data structures that must remain compatible\n- shared runtime or deployment constraints\n- cross-repository migration risks\n- opportunities to decouple repositories before or during modernization\n\nBase recommendations on evidence from the discovered system.\n\nDo not assume that repositories should be merged, split, converted to\nservices, or migrated independently.\n\n## Step C7 — Write the common assessment\n\nCreate:\n\n```text\n<doc_directory>/common/assessment/ASSESSMENT.md\n<doc_directory>/common/assessment/ARCHITECTURE.mmd\n```\n\nWrite `<doc_directory>/common/ASSESSMENT.md` with:\n\n- **System Executive Summary**\n  - what the repositories collectively represent\n  - major relationships\n  - headline system-level risks\n  - headline modernization implication\n\n- **Repository Landscape**\n  - repository\n  - discovered responsibility\n  - technology/platform\n  - main inputs/outputs\n  - relationships\n\n- **Cross-Repository Relationships**\n  - confirmed relationships\n  - evidence\n  - confidence\n\n- **Cross-Repository Execution and Data Flows**\n  - significant end-to-end flows\n\n- **System Architecture-at-a-Glance**\n  - reference the common architecture diagram\n\n- **Shared and Cross-Repository Risks**\n  - findings that cannot be attributed to only one repository\n\n- **System Documentation Gaps**\n  - missing or ambiguous cross-repository knowledge\n\n- **Modernization Dependencies and Sequencing**\n  - dependencies that influence migration planning\n  - coordination requirements\n  - ordering constraints\n\n- **Overall Modernization Pattern**\n  - system-level recommendation\n  - explicitly distinguish it from individual repository recommendations\n    where they differ\n\nFor effort estimation, preserve each repository's independently calculated\nCOCOMO estimate.\n\nIf an overall figure is presented, show the repository estimates separately\nand clearly explain how the overall value was derived.\n\nDo not calculate system effort by treating the repositories as an artificially\nmerged source tree.\n\nWrite `<doc_directory>/common/assessment/ARCHITECTURE.mmd` containing the system-level\nMermaid diagram showing repository boundaries and confirmed relationships.\n\nVerify both common artifacts exist.\n\n---\n\n# Present\n\nReport:\n\n- repositories discovered under `<scan_directory>`\n- repository-level assessment artifacts generated for each repository\n- whether a common system assessment was required\n- common artifacts generated, when applicable\n- unresolved or inferred cross-repository relationships, when applicable\n\nFor each repository suggest:\n\n```text\nglow -p <doc_directory>/<repository-name>/assessment/ASSESSMENT.md\n```\n\nIf more than one repository exists, also suggest:\n\n```text\nglow -p <doc_directory>/common/assessment/ASSESSMENT.md\n```"
}
```

---
