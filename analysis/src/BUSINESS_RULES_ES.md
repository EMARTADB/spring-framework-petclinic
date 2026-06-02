# Especificación de reglas de negocio — Spring PetClinic

> **Generado:** 2026-05-29  
> **Fuente:** `src/main/java` · `src/main/webapp/WEB-INF` · `src/main/resources`  
> **Método:** Tres agentes paralelos de extracción de reglas de negocio (lente de cálculos · lente de validación · lente de ciclo de vida) + verificación contra código fuente  
> **Audiencia:** Ingenieros que heredan este sistema, QA que escribe pruebas de aceptación, arquitectos que planifican una reescritura

---

## Tabla resumen

| ID | Nombre | Categoría | Prioridad | Fuente | Confianza |
|----|--------|-----------|-----------|--------|-----------|
| RULE-001 | Identidad de entidad: nueva vs. persistida | Ciclo de vida | P0 | `BaseEntity.java:43-45` | Alta |
| RULE-002 | Teléfono del propietario: solo dígitos, máximo 10 | Validación | P0 | `Owner.java:54-57` | Alta |
| RULE-003 | Campos obligatorios del propietario (5 campos) | Validación | P1 | `Person.java:31-36`, `Owner.java:46-57` | Alta |
| RULE-004 | El nombre de la mascota es obligatorio | Validación | P1 | `PetValidator.java:43-45` | Alta |
| RULE-005 | Nombre de mascota único por propietario al crear | Validación | P1 | `PetController.java:79-81`, `Owner.java:125-137` | Alta |
| RULE-006 | Tipo de mascota obligatorio solo al crear | Validación | P1 | `PetValidator.java:48-50` | Alta |
| RULE-007 | La fecha de nacimiento de la mascota es obligatoria | Validación | P1 | `PetValidator.java:53-55` | Alta |
| RULE-008 | La descripción de la visita es obligatoria | Validación | P1 | `Visit.java:47` | Alta |
| RULE-009 | La fecha de visita se inicializa a hoy | Cálculo | P1 | `Visit.java:62-64` | Alta |
| RULE-010 | Mascotas del propietario ordenadas A-Z, sin distinguir mayúsculas | Cálculo | P2 | `Owner.java:99-102` | Alta |
| RULE-011 | Visitas de la mascota ordenadas de más reciente a más antigua | Cálculo | P2 | `Pet.java:100-103` | Alta |
| RULE-012 | Especialidades del veterinario ordenadas A-Z, sin distinguir mayúsculas | Cálculo | P2 | `Vet.java:64-66` | Alta |
| RULE-013 | Recuento de especialidades del veterinario derivado | Cálculo | P2 | `Vet.java:69-71` | Alta |
| RULE-014 | Se muestra "none" cuando el veterinario no tiene especialidades | Cálculo | P2 | `vetList.jsp:28` | Alta |
| RULE-015 | Búsqueda de propietario: coincidencia por prefijo | Política | P1 | `JpaOwnerRepositoryImpl.java:56-58` | Alta |
| RULE-016 | Búsqueda con apellido vacío devuelve TODOS los propietarios | Política | P1 | `OwnerController.java:80-82` | Alta |
| RULE-017 | Un único resultado de búsqueda redirige automáticamente | Política | P1 | `OwnerController.java:90-93` | Alta |
| RULE-018 | Búsqueda de propietario: sin resultados → error de validación | Validación | P1 | `OwnerController.java:86-89` | Alta |
| RULE-019 | Los tipos de mascota vienen de datos y se ordenan por nombre | Política | P1 | `JdbcOwnerRepositoryImpl.java:139` | Alta |
| RULE-020 | Lista de veterinarios cacheada; nunca se invalida | Política | P0 | `ClinicServiceImpl.java:100-103` | Alta |
| RULE-021 | INSERT vs UPDATE decidido por nulidad del id | Ciclo de vida | P0 | `BaseEntity.java:43`, `JdbcOwnerRepositoryImpl.java:124` | Alta |
| RULE-022 | Campo `id` bloqueado en el binding web | Validación | P0 | `OwnerController.java:49-51`, `PetController.java:61` | Alta |
| RULE-023 | Mascota enlazada al propietario mediante addPet() | Ciclo de vida | P1 | `Owner.java:104-107` | Alta |
| RULE-024 | La visita es de una sola escritura (sin ruta de actualización) | Ciclo de vida | P1 | `JdbcVisitRepositoryImpl.java:62` | Alta |
| RULE-025 | Los veterinarios son de solo lectura en runtime | Ciclo de vida | P1 | `VetController.java:42-71` | Alta |
| RULE-026 | Borrar propietario elimina en cascada todas sus mascotas (solo JPA) | Ciclo de vida | P0 | `Owner.java:59` | Media |
| RULE-027 | Borrar mascota elimina en cascada todas sus visitas (solo JPA) | Ciclo de vida | P0 | `Pet.java:55` | Media |
| RULE-028 | No existe soft-delete para ninguna entidad | Ciclo de vida | P1 | schema.sql (ausencia) | Alta |
| RULE-029 | Sin bloqueo optimista / sin versionado | Ciclo de vida | P1 | Todos los modelos (ausencia) | Alta |
| RULE-030 | Formato de fecha: entrada `yyyy/MM/dd`, visualización `yyyy-MM-dd` | Cálculo | P2 | `Pet.java:49`, `ownerDetails.jsp:54` | Alta |
| RULE-031 | Teléfono máximo 10 dígitos, sin mínimo | Validación | P1 | `Owner.java:55-57` | Alta |
| RULE-032 | Comprobación de duplicado de nombre de mascota omitida al actualizar | **Defecto sospechado** | P1 | `PetController.java:79` | Alta |
| RULE-033 | Tipo de mascota no revalidado al actualizar | **Defecto sospechado** | P0 | `PetValidator.java:48-50` | Alta |
| RULE-034 | Fecha de visita: sin restricción pasado/futuro | **Defecto sospechado** | P1 | `VisitController.java` (ausencia) | Alta |
| RULE-035 | Apellido del propietario almacenado sin distinguir mayúsculas en H2 | Política | P1 | `h2/schema.sql:39` | Alta |
| RULE-036 | Datos de referencia iniciales: 6 tipos de mascota, 3 especialidades | Política | P2 | `db/h2/data.sql` | Alta |

---

## CÁLCULOS

### RULE-009: La fecha de visita se inicializa a hoy
**Categoría:** Cálculo  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Visit.java:62-64`  
**Explicación:** Cuando se crea una visita nueva, su fecha se establece automáticamente al día natural actual; el clínico puede cambiarla antes de guardar.

**Especificación:**
```
Dado que se instancia un nuevo objeto Visit
Cuando se ejecuta el constructor sin argumentos Visit()
Entonces this.date = LocalDate.now()
Y el campo fecha es editable en el formulario antes del envío
Y no se aplica ningún límite mínimo ni máximo de fecha
```

**Parámetros:**
- Fuente de fecha: `LocalDate.now()` — reloj del sistema de la JVM, sin sobrescritura de zona horaria.
- Formato para binding: `yyyy/MM/dd` (`@DateTimeFormat(pattern="yyyy/MM/dd")`).

**Casos borde gestionados:** Ninguno. El validador acepta fecha `null` porque no hay `@NotNull` en `Visit.date`.

**Defecto sospechado:** El validador no rechaza `null`, fechas futuras ni fechas anteriores al nacimiento de la mascota. Una visita programada para 2099-01-01 se guarda sin error.

**Confianza:** Alta

---

### RULE-010: Las mascotas del propietario se muestran ordenadas A-Z, sin distinguir mayúsculas
**Categoría:** Cálculo  
**Prioridad:** P2  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Owner.java:99-102`  
**Explicación:** Siempre que se listan las mascotas de un propietario —en la página de detalle o en formularios— aparecen alfabéticamente por nombre de mascota, independientemente del orden en que se registraron.

**Especificación:**
```
Dado un Owner con mascotas ["Zara", "basil", "Leo"] en orden de inserción
Cuando se llama a owner.getPets()
Entonces la lista devuelta es ["basil", "Leo", "Zara"] (A-Z sin distinguir mayúsculas)
Y la lista es inmutable (Collections.unmodifiableList)
```

**Parámetros:**
- Comparador: `Comparator.comparing(Pet::getName, String.CASE_INSENSITIVE_ORDER)`.
- Tipo devuelto: `Collections.unmodifiableList` — los llamadores no pueden mutarla.

**Casos borde gestionados:** Comparación sin distinguir mayúsculas (`"basil"` se ordena antes que `"Leo"`).

**Confianza:** Alta

---

### RULE-011: Las visitas de la mascota se muestran de más reciente a más antigua
**Categoría:** Cálculo  
**Prioridad:** P2  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Pet.java:100-103`  
**Explicación:** El historial de visitas de una mascota siempre se muestra con la visita más reciente arriba.

**Especificación:**
```
Dada una Pet con visitas en 2024-01-10, 2023-06-15, 2025-03-01
Cuando se llama a pet.getVisits()
Entonces la lista devuelta es [2025-03-01, 2024-01-10, 2023-06-15] (descendente por fecha)
Y la lista es inmutable
```

**Parámetros:**
- Comparador: `Comparator.comparing(Visit::getDate).reversed()`.
- Almacenamiento: `Set<Visit>` interno sin orden; el orden se calcula en cada llamada a `getVisits()`.

**Casos borde gestionados:** Ninguno para empates en la misma fecha; el orden entre visitas del mismo día no es determinista.

**Confianza:** Alta

---

### RULE-012: Las especialidades del veterinario se muestran A-Z, sin distinguir mayúsculas
**Categoría:** Cálculo  
**Prioridad:** P2  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Vet.java:64-66`  
**Explicación:** Las especialidades de un veterinario aparecen en orden alfabético en la vista de lista de veterinarios.

**Especificación:**
```
Dado un Vet con especialidades ["surgery", "Dentistry", "radiology"]
Cuando se llama a vet.getSpecialties()
Entonces la lista devuelta es ["Dentistry", "radiology", "surgery"] (A-Z sin distinguir mayúsculas)
Y la lista es inmutable
```

**Parámetros:**
- Comparador: `Comparator.comparing(Specialty::getName, String.CASE_INSENSITIVE_ORDER)`.

**Confianza:** Alta

---

### RULE-013: El recuento de especialidades del veterinario se deriva del tamaño del conjunto
**Categoría:** Cálculo  
**Prioridad:** P2  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Vet.java:69-71`  
**Explicación:** El número de especialidades que tiene un veterinario se calcula contando el conjunto de especialidades; no se almacena en una columna.

**Especificación:**
```
Dado un Vet con 2 entradas en la tabla de unión vet_specialties
Cuando se llama a vet.getNrOfSpecialties()
Entonces se devuelve 2 (getSpecialtiesInternal().size())
```

**Parámetros:** No hay umbral hardcodeado. Tener cero especialidades es un estado válido.

**Casos borde gestionados:** Cero devuelve 0, no null. No se aplica un máximo de especialidades.

**Confianza:** Alta

---

### RULE-014: Cero especialidades se muestra como "none"
**Categoría:** Cálculo  
**Prioridad:** P2  
**Fuente:** `src/main/webapp/WEB-INF/jsp/vets/vetList.jsp:28`  
**Explicación:** Cuando un veterinario no tiene especialidades, la UI muestra literalmente la palabra "none" en vez de una celda vacía.

**Especificación:**
```
Dado un Vet donde getNrOfSpecialties() == 0
Cuando se renderiza la página de lista de veterinarios
Entonces la celda de especialidades muestra "none"

Dado un Vet donde getNrOfSpecialties() > 0
Cuando se renderiza la página de lista de veterinarios
Entonces se muestra cada nombre de especialidad, separado por comas
```

**Confianza:** Alta

---

### RULE-030: Formatos de fecha — entrada y visualización difieren
**Categoría:** Cálculo  
**Prioridad:** P2  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Pet.java:49` (entrada) · `src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp:54` (visualización)  
**Explicación:** Las fechas se introducen en formato `yyyy/MM/dd`, separado por barras, pero se muestran en formato `yyyy-MM-dd`, separado por guiones. Son dos formatos distintos para el mismo dato.

**Especificación:**
```
Dado que un usuario escribe "2020/03/08" en el campo de fecha de nacimiento
Cuando se envía el formulario
Entonces el valor se enlaza a LocalDate 2020-03-08 (vía @DateTimeFormat(pattern="yyyy/MM/dd"))

Dado que la página de detalle del propietario renderiza esta mascota
Cuando se ejecuta <pet:localDate value="${pet.birthDate}" pattern="yyyy-MM-dd"/>
Entonces la visualización muestra "2020-03-08"
```

**Parámetros:**
- Formato de entrada: `yyyy/MM/dd`.
- Formato de visualización: `yyyy-MM-dd`.
- Mensaje de error en fallo de parseo: `typeMismatch.birthDate` → `"invalid date"` (`messages.properties:8`).

**Defecto sospechado:** La inconsistencia entre formato de entrada y formato de visualización puede confundir al usuario. Un usuario que copia `"2020-03-08"` desde la página de detalle y lo pega en el formulario obtiene un error de parseo.

**Confianza:** Alta

---

## VALIDACIONES

### RULE-001: Máquina de estados de identidad de entidad
**Categoría:** Ciclo de vida  
**Prioridad:** P0  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java:43-45`  
**Explicación:** Cada objeto de dominio está en estado NUEVO, nunca guardado y con `id` null, o PERSISTIDO, con un identificador entero asignado por la base de datos. Este único dato decide INSERT frente a UPDATE en todas las pilas de persistencia.

**Especificación:**
```
Dado cualquier objeto de dominio (Owner, Pet, Visit, Vet, Specialty, PetType)
Cuando se llama a isNew()
Entonces devuelve true si y solo si this.id == null

Dada una entidad NUEVA que se pasa a save()
Cuando save() se ejecuta
Entonces se lanza un INSERT SQL y la BD asigna un id generado a this.id
Y llamadas posteriores a isNew() devuelven false

Dada una entidad PERSISTIDA (id != null) que se pasa a save()
Cuando save() se ejecuta
Entonces se lanza un UPDATE SQL
Y el id no cambia
```

**Parámetros:** `GenerationType.IDENTITY` — secuencia nativa de la base de datos. No hay generación de identificadores a nivel de aplicación.

**Casos borde gestionados:** Ninguno explícitamente. Un objeto con `id` asignado manualmente a una PK inexistente intentará un UPDATE que en modo JDBC afectará silenciosamente a 0 filas.

**Defecto sospechado:** Las implementaciones de repositorio JPA (`JpaOwnerRepositoryImpl.java:73`, `JpaPetRepositoryImpl.java:58`) comprueban `id == null` directamente en vez de llamar a `isNew()`, lo que crea divergencia de mantenimiento.

**Confianza:** Alta

---

### RULE-002: Teléfono del propietario — solo dígitos numéricos, máximo 10 dígitos
**Categoría:** Validación  
**Prioridad:** P0  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Owner.java:54-57`  
**Explicación:** Un número de teléfono solo puede contener caracteres de dígito y no puede tener más de 10 dígitos en total; no se permiten separadores ni prefijos de país.

**Especificación:**
```
Dado un formulario Owner enviado con telephone = "6085551023"
Cuando valida @Digits(fraction=0, integer=10)
Entonces se acepta el valor (10 dígitos, sin decimales)

Dado telephone = "608-555-1023"
Cuando valida @Digits
Entonces se rechaza: no se permiten caracteres no numéricos
Mensaje de error: "numeric value out of bounds (<10 digits>.<0 digits> expected)"

Dado telephone = "12345678901" (11 dígitos)
Cuando valida @Digits
Entonces se rechaza: supera integer=10
```

**Parámetros:**
- `integer = 10` — cantidad máxima de dígitos, hardcodeada.
- `fraction = 0` — no se permite parte decimal.
- Columna BD: `VARCHAR(20)` — la columna es más amplia que el máximo validado; la BD aceptaría valores más largos si se evita la validación.

**Casos borde gestionados:** `null` y cadena vacía son capturados antes por `@NotEmpty` (RULE-003).

**Defecto sospechado:** No se exige longitud mínima. Un único dígito `"1"` pasa tanto `@NotEmpty` como `@Digits`. No hay formato con prefijo de país ni estructura de código de área. Los números internacionales se rechazan salvo que tengan 10 dígitos o menos.

**Confianza:** Alta — la regla es clara e intencional. La idoneidad del máximo de 10 dígitos para el negocio es una **pregunta para SME**.

---

### RULE-003: Campos obligatorios del propietario (5 campos)
**Categoría:** Validación  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Person.java:31-36`, `src/main/java/org/springframework/samples/petclinic/model/Owner.java:46-57`  
**Explicación:** Un registro de propietario no puede guardarse sin nombre, apellido, dirección, ciudad y teléfono; los cinco campos son obligatorios.

**Especificación:**
```
Dado un formulario Owner enviado con cualquiera de estos campos en blanco:
  firstName, lastName, address, city, telephone
Cuando valida @NotEmpty (disparado por @Valid en el controlador)
Entonces se rechaza el formulario con error de campo "is required"
Y no se escribe en BD
Y el formulario se vuelve a renderizar con el error junto al campo vacío

Dado que los cinco campos no están vacíos
Cuando la validación pasa
Entonces el propietario se guarda (INSERT o UPDATE)
```

**Parámetros:**
- Anotación: `@NotEmpty` (Jakarta Validation) — rechaza `null`, `""` y cadenas solo con espacios.
- Clave de mensaje de error: no hay clave en `messages.properties` para `@NotEmpty`; usa el valor por defecto de Jakarta Validation → **"must not be empty"**.
- Restricción en BD: **ninguna** — las columnas `first_name`, `last_name`, `address`, `city`, `telephone` aceptan null a nivel de BD. La validación solo existe en la aplicación.

**Casos borde gestionados:** Cadenas compuestas solo por espacios (`"   "`) son rechazadas por `@NotEmpty`.

**Defecto sospechado:** No hay `@Size(max=30)` en `firstName`/`lastName` aunque las columnas son `VARCHAR(30)`. Un nombre de 31 caracteres pasa la validación de aplicación, pero provoca truncado o error de BD al guardar.

**Confianza:** Alta

---

### RULE-004: El nombre de la mascota es obligatorio
**Categoría:** Validación  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/PetValidator.java:43-45`  
**Explicación:** Una mascota no puede crearse ni actualizarse sin nombre.

**Especificación:**
```
Dado un formulario Pet enviado con name = "" o name = null
Cuando se ejecuta PetValidator.validate()
Entonces se dispara errors.rejectValue("name", "required", "required")
Y el formulario se vuelve a renderizar con error "is required" en el campo Name

Dado name = "Basil"
Cuando PetValidator valida
Entonces la comprobación del nombre pasa y continúan las demás comprobaciones
```

**Parámetros:**
- Validador: `PetValidator` (interfaz `Validator` de Spring, no Bean Validation).
- Cableado mediante: `@InitBinder("pet")` en `PetController.java:66`.
- Código de error: `required` → `messages.properties:2` → **"is required"**.
- Restricción en BD: `pets.name VARCHAR(30)` — sin NOT NULL.

**Casos borde gestionados:** `null`, `""` y cadenas solo con espacios fallan con `StringUtils.hasLength()`.

**Confianza:** Alta

---

### RULE-005: El nombre de mascota debe ser único por propietario al crear, sin distinguir mayúsculas
**Categoría:** Validación  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/PetController.java:79-81`, `src/main/java/org/springframework/samples/petclinic/model/Owner.java:125-137`  
**Explicación:** Un propietario no puede registrar dos mascotas con el mismo nombre. La comparación no distingue mayúsculas. Esta regla solo aplica al crear una mascota nueva, no al editar una existente.

**Especificación:**
```
Dado que Owner "John" tiene una mascota existente llamada "Basil" (persistida)
Cuando se envía una nueva Pet con name = "basil" para ese propietario
Entonces owner.getPet("basil", true) encuentra la "Basil" existente (ignoreNew=true omite mascotas sin guardar)
Y se dispara result.rejectValue("name", "duplicate", "already exists")
Y no se realiza INSERT

Dado que Owner "John" no tiene ninguna mascota llamada "Basil"
Cuando se envía una nueva Pet con name = "Basil"
Entonces owner.getPet("Basil", true) devuelve null
Y no se lanza error de duplicado
Y el INSERT continúa

Dada una mascota PERSISTIDA llamada "Basil" que se edita con name = "Leo" (nombre de otra mascota)
Cuando se envía el formulario de actualización
Entonces la comprobación de duplicados NO se realiza (pet.isNew() == false → el guard la omite)
Y la actualización continúa, creando dos mascotas con nombre "Leo" para este propietario
```

**Parámetros:**
- Comparación: `String.toLowerCase()` en ambos lados — lower-case con locale por defecto.
- `ignoreNew=true` en la llamada a `getPet()` — las mascotas nuevas no guardadas se excluyen de la comparación, por lo que la mascota que se está creando no entra en conflicto consigo misma.

**Defecto sospechado:** El guard `pet.isNew()` en `PetController.java:79` implica que la comprobación de duplicados está totalmente ausente en actualizaciones. Una edición puede renombrar una mascota y hacerla coincidir con una hermana. Parece no intencional — **requiere confirmación de SME**.

**Confianza:** Alta, porque el código es inequívoco. La intención sobre el comportamiento en actualización es **Media**; ver preguntas para SME.

---

### RULE-006: El tipo de mascota es obligatorio al crear; no se revalida al actualizar
**Categoría:** Validación  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/PetValidator.java:48-50`  
**Explicación:** Al registrar una mascota nueva debe seleccionarse un tipo de mascota, como gato o perro. Al editar una mascota existente, el campo tipo no se vuelve a comprobar; puede quedar vacío.

**Especificación:**
```
Dado un formulario de nueva Pet enviado con type = null
Cuando pet.isNew() == true Y pet.getType() == null
Entonces se dispara errors.rejectValue("type", "required", "required")
Y el formulario se vuelve a renderizar con "is required" en Type

Dado un formulario de Pet existente enviado con type = null
Cuando pet.isNew() == false
Entonces se omite la comprobación de tipo (condición: pet.isNew() && pet.getType() == null)
Y save() se ejecuta con type = null
  → En modo JDBC: NullPointerException en JdbcPetRepositoryImpl.java:113 (pet.getType().getId())
  → En modo JPA: violación de restricción de BD (pets.type_id NOT NULL)
```

**Parámetros:**
- Restricción en BD: `pets.type_id INTEGER NOT NULL` — se aplica a nivel de BD en cualquier perfil.

**Defecto sospechado:** El guard `pet.isNew()` crea una ventana en la que el tipo puede vaciarse al editar, causando un crash en runtime en JDBC o una violación de constraint en JPA, en lugar de un error amigable en el formulario. **Esto es un bug.** Ver preguntas para SME.

**Confianza:** Alta

---

### RULE-007: La fecha de nacimiento de la mascota es obligatoria
**Categoría:** Validación  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/PetValidator.java:53-55`  
**Explicación:** Debe proporcionarse la fecha de nacimiento de una mascota al crear o actualizar su registro.

**Especificación:**
```
Dado un formulario Pet enviado con birthDate = null
Cuando PetValidator valida
Entonces se dispara errors.rejectValue("birthDate", "required", "required")
Y el formulario se vuelve a renderizar con "is required" en Birth Date

Dado birthDate = "2020/03/08" (formato válido)
Cuando @DateTimeFormat(pattern="yyyy/MM/dd") parsea correctamente
Entonces se enlaza el valor LocalDate y PetValidator recibe un birthDate no null
Y no se lanza error de fecha de nacimiento
```

**Parámetros:**
- Formato de parseo: `yyyy/MM/dd`, separado por barras.
- Error de fallo de parseo: `typeMismatch.birthDate` → **"invalid date"**.
- No hay límite de fecha pasada o futura.

**Defecto sospechado:** Se aceptan fechas de nacimiento futuras sin error, por ejemplo `2099/12/31`. También se aceptan fechas anteriores a los datos semilla de la base de datos o anteriores a 1900.

**Confianza:** Alta

---

### RULE-008: La descripción de la visita es obligatoria
**Categoría:** Validación  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Visit.java:47`  
**Explicación:** Cada visita debe tener una descripción; no se pueden guardar visitas en blanco.

**Especificación:**
```
Dado un formulario Visit enviado con description = "" o null
Cuando valida @NotEmpty sobre Visit.description
Entonces se rechaza el formulario con "must not be empty" en el campo Description
Y no se realiza INSERT

Dado description = "Annual checkup and vaccinations"
Cuando la validación pasa
Entonces se ejecuta saveVisit() y la visita se persiste
```

**Parámetros:**
- Anotación: `@NotEmpty` (Jakarta Bean Validation).
- Columna BD: `visits.description VARCHAR(255)` — sin NOT NULL a nivel de BD.
- No hay longitud máxima en la capa de aplicación; la BD limita a 255 caracteres, con posible truncado o error.

**Confianza:** Alta

---

### RULE-018: Búsqueda de propietario — sin resultados produce error de campo
**Categoría:** Validación  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/OwnerController.java:86-89`  
**Explicación:** Si una búsqueda por apellido no encuentra propietarios, se vuelve a mostrar el formulario con un error en el campo Last Name en lugar de mostrar una lista vacía.

**Especificación:**
```
Dado lastName = "Nonexistent"
Cuando findOwnerByLastName("Nonexistent%") devuelve una colección vacía
Entonces se dispara result.rejectValue("lastName", "notFound", "not found")
Y el formulario Find Owners se vuelve a renderizar
Y el campo "Last name" muestra el error "has not been found"
```

**Parámetros:**
- Código de error: `notFound` → `messages.properties:3` → **"has not been found"**.

**Confianza:** Alta

---

### RULE-022: El campo `id` se bloquea en el binding de formularios web
**Categoría:** Validación  
**Prioridad:** P0  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/OwnerController.java:49-51`, `src/main/java/org/springframework/samples/petclinic/web/PetController.java:61`  
**Explicación:** Un cliente no puede enviar un valor de clave primaria mediante un formulario; el campo `id` siempre se elimina de las peticiones entrantes para prevenir ataques de asignación masiva.

**Especificación:**
```
Dado un POST a /owners/new con un campo oculto id=999 en el body
Cuando @InitBinder ejecuta dataBinder.setDisallowedFields("id")
Entonces el valor id=999 se descarta silenciosamente
Y el objeto Owner enlazado desde el formulario tiene id = null
Y la BD asigna un id autogenerado real en el INSERT

Dado un POST a /owners/{ownerId}/edit
Cuando el binder elimina id
Entonces ownerId de la URL se reaplica manualmente mediante owner.setId(ownerId) en OwnerController.java:114
```

**Parámetros:** Se aplica tanto a `OwnerController` para binding de owner como a `PetController` para binding de owner mediante `@InitBinder("owner")`. Los formularios de Visit y Vet no exponen campo `id`, así que no necesitan binder.

**Confianza:** Alta

---

## POLÍTICAS

### RULE-015: La búsqueda por apellido de propietario usa coincidencia por prefijo
**Categoría:** Política  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaOwnerRepositoryImpl.java:56-58`, `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcOwnerRepositoryImpl.java:76-77`  
**Explicación:** Buscar propietarios por apellido devuelve cualquier propietario cuyo apellido empieza por el texto introducido; no es una búsqueda exacta ni de contenido intermedio.

**Especificación:**
```
Dados propietarios con apellidos: "Davis", "Davidson", "Smith"
Cuando el usuario busca lastName = "Dav"
Entonces findOwnerByLastName devuelve ["Davis", "Davidson"] (ambos empiezan por "Dav")
Y "Smith" no se devuelve

Dado lastName = "" (cadena vacía)
Cuando OwnerController establece lastName = "" (RULE-016)
Entonces se ejecuta SQL WHERE last_name LIKE '%' → se devuelven TODOS los propietarios
```

**Parámetros:**
- SQL: `WHERE last_name like :lastName` con parámetro `lastName + "%"`, añadiendo comodín.
- Tipo de columna en H2: `VARCHAR_IGNORECASE(30)` → la búsqueda no distingue mayúsculas en H2.
- MySQL/PostgreSQL: la sensibilidad a mayúsculas depende de la colación; no se garantiza búsqueda case-insensitive.

**Defecto sospechado:** La insensibilidad a mayúsculas es un efecto lateral del tipo de columna H2, no una decisión explícita en la aplicación. En MySQL con colación sensible a mayúsculas, esta búsqueda pasaría a distinguir mayúsculas; habría divergencia de comportamiento entre perfiles de base de datos.

**Confianza:** Alta para el comportamiento en H2. **Media** para consistencia entre bases de datos; SME debe confirmar la política de sensibilidad a mayúsculas.

---

### RULE-016: La búsqueda con apellido vacío devuelve todos los propietarios, sin paginación
**Categoría:** Política  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/OwnerController.java:80-82`  
**Explicación:** Si un usuario envía el formulario Find Owner sin escribir nada, se devuelven todos los propietarios de la base de datos.

**Especificación:**
```
Dado que se envía el formulario Find Owner sin valor lastName
Cuando OwnerController comprueba: if (owner.getLastName() == null) → setLastName("")
Entonces se llama a findOwnerByLastName("")
Y se ejecuta SQL: WHERE last_name LIKE '%'
Y TODOS los propietarios se devuelven en un único result set sin paginar
```

**Parámetros:** Sin límite de página. Sin tope de filas. Todos los propietarios de la base de datos se cargan en memoria.

**Defecto sospechado:** Una clínica con miles de propietarios cargará todos en el heap de Java ante una búsqueda en blanco. Es un límite de escalabilidad: no hay paginación ni cláusula LIMIT.

**Confianza:** Alta

---

### RULE-017: Un único resultado de búsqueda redirige automáticamente al detalle del propietario
**Categoría:** Política  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/OwnerController.java:90-93`  
**Explicación:** Si una búsqueda encuentra exactamente un propietario, el sistema navega directamente a la página de detalle de ese propietario, saltándose la vista de lista.

**Especificación:**
```
Dado lastName = "Carter"
Cuando findOwnerByLastName devuelve exactamente 1 Owner
Entonces OwnerController devuelve inmediatamente "redirect:/owners/{id}"
Y no se renderiza ownersList.jsp

Dado lastName = "Davis"
Cuando findOwnerByLastName devuelve 2+ Owners
Entonces se establece el atributo de modelo "selections"
Y ownersList.jsp se renderiza mostrando todos los propietarios coincidentes
```

**Confianza:** Alta

---

### RULE-019: Los tipos de mascota son datos de referencia y se recuperan ordenados por nombre
**Categoría:** Política  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcOwnerRepositoryImpl.java:139`  
**Explicación:** La lista de tipos de mascota disponibles se carga desde la base de datos, no está hardcodeada. Los tipos aparecen en el desplegable ordenados alfabéticamente por nombre.

**Especificación:**
```
Dado que la tabla types contiene: cat, dog, hamster, lizard, snake, bird
Cuando se llama a findPetTypes()
Entonces SQL: SELECT id, name FROM types ORDER BY name
Entonces los tipos se devuelven ordenados: [bird, cat, dog, hamster, lizard, snake]
Y esta lista alimenta el desplegable Type del formulario Pet
```

**Parámetros:**
- Datos semilla (`h2/data.sql`): cat, dog, lizard, bird, hamster, snake (6 tipos).
- No hay caché de aplicación en `findPetTypes()`; se consulta la BD en cada renderizado del formulario de mascota.

**Defecto sospechado:** `findPetTypes()` no está cacheado aunque es dato de referencia prácticamente estático. Cada renderizado del formulario de mascota ejecuta un `SELECT` sobre la tabla `types`. Añadir `@Cacheable("petTypes")` eliminaría esto.

**Confianza:** Alta

---

### RULE-020: La lista de veterinarios se cachea indefinidamente, sin invalidación
**Categoría:** Política  
**Prioridad:** P0  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java:100-103`  
**Explicación:** El censo completo de veterinarios se carga desde la base de datos una vez y se cachea en memoria durante toda la vida de la aplicación; cualquier cambio en veterinarios en la BD es invisible hasta reiniciar la aplicación.

**Especificación:**
```
Dado que la caché "vets" de Caffeine está vacía (arranque en frío o primera petición)
Cuando se llama a GET /vets
Entonces vetRepository.findAll() ejecuta una lectura completa de BD (con especialidades cargadas EAGER)
Y la lista resultado se almacena en la caché "vets"

Dado que la caché "vets" está caliente
Cuando se llama de nuevo a GET /vets, cualquier número de veces
Entonces NO se consulta la BD; se devuelve la lista cacheada

Dado que se inserta directamente un nuevo Vet en la BD mientras la app está ejecutándose
Cuando se llama a GET /vets
Entonces el nuevo Vet NO es visible; no existe ningún @CacheEvict en el código
Y la única forma de ver el nuevo Vet es reiniciar la aplicación
```

**Parámetros:**
- Nombre de caché: `"vets"` (literal en `ClinicServiceImpl.java:100`).
- Proveedor de caché: Caffeine, configurado mediante `spring-context-support`.
- Política de invalidación: **ninguna** — sin TTL, sin `@CacheEvict`, sin `@CachePut`.

**Defecto sospechado:** La caché permanente solo tiene sentido si los veterinarios son configuración realmente inmutable. Si se añade una funcionalidad de crear veterinarios, esta caché necesitará estrategia de invalidación. Es un defecto latente en cualquier modernización que amplíe la gestión de veterinarios.

**Confianza:** Alta

---

### RULE-035: El apellido del propietario se almacena sin distinguir mayúsculas en H2
**Categoría:** Política  
**Prioridad:** P1  
**Fuente:** `src/main/resources/db/h2/schema.sql:39`  
**Explicación:** En la base de datos H2, los apellidos de propietarios se almacenan y buscan sin tener en cuenta mayúsculas; `"Davis"` y `"davis"` se tratan de forma idéntica.

**Especificación:**
```
Dado un Owner guardado con lastName = "Davis"
Cuando se ejecuta una búsqueda por lastName = "davis" en H2
Entonces el propietario SÍ se encuentra (columna VARCHAR_IGNORECASE)

Dados los mismos datos en MySQL o PostgreSQL
Cuando se ejecuta una búsqueda por lastName = "davis"
Entonces la sensibilidad a mayúsculas depende de la base de datos/colación; no está garantizada
```

**Parámetros:** Tipo de columna H2: `VARCHAR_IGNORECASE(30)`. MySQL/PostgreSQL usan `VARCHAR`, dependiente de colación.

**Defecto sospechado:** La garantía de insensibilidad a mayúsculas es específica de la BD. Una migración de H2 a MySQL sin colación case-insensitive cambia el comportamiento observable de búsqueda.

**Confianza:** Alta

---

### RULE-036: Datos de referencia iniciales en el arranque
**Categoría:** Política  
**Prioridad:** P2  
**Fuente:** `src/main/resources/db/h2/data.sql`  
**Explicación:** Se insertan seis tipos de mascota y tres especialidades veterinarias en la base de datos al arrancar la aplicación.

**Especificación:**
```
Dada una base de datos fresca
Cuando la aplicación arranca con el perfil H2
Entonces se insertan estos 6 tipos: cat, dog, lizard, bird, hamster, snake
Y estas 3 especialidades: radiology, surgery, dentistry
Y estos 6 veterinarios: Carter, Leary, Douglas, Ortega, Stevens, Jenkins
Y las asignaciones de especialidad son: Leary→radiology, Douglas→surgery+dentistry, Ortega→surgery, Stevens→radiology
```

**Parámetros:** Todos los valores están hardcodeados en `data.sql`. No hay UI de administración para añadir tipos o especialidades.

**Confianza:** Alta

---

## CICLO DE VIDA

### RULE-021: INSERT vs. UPDATE decidido por nulidad del id
**Categoría:** Ciclo de vida  
**Prioridad:** P0  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcOwnerRepositoryImpl.java:124`, `src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaOwnerRepositoryImpl.java:73-79`  
**Explicación:** Que una operación de guardado inserte una fila nueva o actualice una existente se determina por si el campo `id` de la entidad es null.

**Especificación:**
```
Dada una entidad con id == null
Cuando se llama a save()
Entonces se ejecuta INSERT SQL
Y el id entero generado por la BD se asigna a entity.id

Dada una entidad con id != null
Cuando se llama a save()
Entonces se ejecuta UPDATE SQL
Y se actualiza la fila con el id correspondiente
Y el id no cambia

Dada una entidad con id establecido a un valor que no existe en la BD
Cuando se llama a save() en la ruta JDBC
Entonces se ejecuta UPDATE SQL, pero afecta a 0 filas
Y no se lanza error: pérdida de datos silenciosa
```

**Parámetros:** Aplica a Owner, Pet, Visit. En JPA: `em.persist()` vs `em.merge()`; en JDBC: comprobación `isNew()`.

**Casos borde gestionados:** JPA gestiona esto mediante `EntityManager.persist()` para nuevos y `merge()` para existentes. JDBC usa `isNew()` para bifurcar entre `SimpleJdbcInsert.executeAndReturnKey()` y un UPDATE con `JdbcClient`.

**Defecto sospechado:** La ruta JDBC no verifica que un UPDATE afecte al menos a 1 fila. Un `id` obsoleto que ya no existe en la BD causa un no-op silencioso.

**Confianza:** Alta

---

### RULE-023: La mascota debe enlazarse al propietario mediante `addPet()`
**Categoría:** Ciclo de vida  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Owner.java:104-107`  
**Explicación:** Una mascota se conecta a su propietario mediante el método `addPet()`, que establece la relación bidireccional; se actualizan atómicamente tanto la colección de mascotas del propietario como la referencia de propietario de la mascota.

**Especificación:**
```
Dado un Owner existente y una nueva Pet
Cuando se llama a owner.addPet(pet)
Entonces pet se añade a owner.petsInternal (Set<Pet>)
Y pet.owner se establece a este owner (vía pet.setOwner(this))
Y ambos lados de la relación bidireccional JPA quedan consistentes

Dado que se llama a savePet(pet) sin owner.addPet() previo
Entonces en modo JDBC: NullPointerException en pet.getOwner().getId() (JdbcPetRepositoryImpl.java:114)
Entonces en modo JPA: pet.owner es null → violación de restricción de BD (owner_id NOT NULL)
```

**Parámetros:**
- Cascada JPA: `Owner.pets` tiene `CascadeType.ALL`; guardar Owner puede guardar en cascada sus mascotas.
- JDBC: no hay cascada; la mascota debe guardarse explícitamente.

**Confianza:** Alta

---

### RULE-024: La visita es de una sola escritura: no existe ruta de actualización ni borrado
**Categoría:** Ciclo de vida  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcVisitRepositoryImpl.java:62`  
**Explicación:** Una vez guardada una visita, no puede modificarse ni eliminarse mediante la aplicación. La implementación JDBC lanza explícitamente una excepción si se intenta una actualización; no existe endpoint web para actualizar o borrar en ninguna ruta de persistencia.

**Especificación:**
```
Dada una Visit guardada con id=42
Cuando cualquier código llama a JdbcVisitRepository.save(visit) con visit.isNew() == false
Entonces se lanza UnsupportedOperationException: "Visit update not supported"

Dada una Visit guardada
Cuando el usuario busca un enlace "Edit Visit" en la UI
Entonces no existe tal enlace: VisitController no tiene mapping GET/POST para actualización de visita
Y no existe endpoint de borrado

Nota: JpaVisitRepositoryImpl.save() usa em.merge() y SÍ soportaría actualización
si existiera un endpoint de controlador. Esto crea una divergencia de comportamiento entre perfiles.
```

**Parámetros:**
- JDBC: la actualización lanza `UnsupportedOperationException` en `JdbcVisitRepositoryImpl.java:62`.
- JPA: la actualización tendría éxito silenciosamente si se activara.
- Spring Data JPA: la actualización tendría éxito mediante `save()` sobre una entidad gestionada.

**Defecto sospechado:** Divergencia de comportamiento entre perfiles: la invariante de "visitas inmutables" solo se fuerza en la capa JDBC. Una modernización que consolide a JPA o Spring Data JPA sin añadir este guard permitiría accidentalmente modificar visitas.

**Confianza:** Alta

---

### RULE-025: Los veterinarios son de solo lectura en runtime
**Categoría:** Ciclo de vida  
**Prioridad:** P1  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/web/VetController.java:42-71`  
**Explicación:** No hay endpoint web para crear, actualizar o borrar veterinarios o especialidades. Los veterinarios son datos de configuración gestionados fuera de la aplicación, mediante inserts directos en BD o scripts de migración.

**Especificación:**
```
Dada la aplicación en ejecución
Cuando cualquier cliente HTTP solicita una URL para crear o editar un Vet
Entonces no existe esa ruta: VetController solo tiene GET /vets, /vets.json, /vets.xml
Y Vet.addSpecialty() existe en el modelo pero nunca se llama desde ningún controlador
```

**Confianza:** Alta

---

### RULE-026: Borrar un propietario elimina en cascada todas sus mascotas en modo JPA
**Categoría:** Ciclo de vida  
**Prioridad:** P0  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Owner.java:59`  
**Explicación:** En modo JPA/Spring Data JPA, borrar un Owner eliminará automáticamente todas sus mascotas. Esta cascada no existe en la pila JDBC, creando una divergencia de comportamiento.

**Especificación:**
```
Dado Owner con id=1 y mascotas [Basil(id=5), Leo(id=6)]
Cuando se llama a em.remove(owner) en modo JPA
Entonces también se borran las mascotas Basil y Leo (CascadeType.ALL incluye REMOVE)
Y se borran todas las visitas de Basil y Leo (Pet también tiene CascadeType.ALL sobre visits)

Dado el mismo escenario en modo JDBC
Cuando se llama a JdbcOwnerRepository.delete() si existiera tal método
Entonces la restricción FK fk_pets_owners IMPEDIRÍA borrar la fila owner
Salvo que las mascotas se borren manualmente antes
```

**Parámetros:** `@OneToMany(cascade = CascadeType.ALL, mappedBy = "owner")` en `Owner.pets` (`Owner.java:59`).

**Casos borde gestionados:** No existe endpoint de borrado en ningún controlador; esta cascada no puede dispararse desde la UI. El riesgo se materializa solo si se añade un endpoint de borrado en una reescritura.

**Confianza:** Media — la anotación de cascada es evidente en código, pero confirmar si este comportamiento es intencional para una clínica en producción requiere **confirmación de SME**.

---

### RULE-027: Borrar una mascota elimina en cascada todas sus visitas en modo JPA
**Categoría:** Ciclo de vida  
**Prioridad:** P0  
**Fuente:** `src/main/java/org/springframework/samples/petclinic/model/Pet.java:55`  
**Explicación:** En modo JPA, borrar una Pet eliminará automáticamente todos los registros de visitas asociados a esa mascota.

**Especificación:**
```
Dada Pet con id=5 y visitas [2024-01-10 "Checkup", 2023-06-15 "Vaccination"]
Cuando se llama a em.remove(pet) en modo JPA
Entonces ambos registros de visita se borran (CascadeType.ALL)
Y el historial de visitas se pierde permanentemente

Dado el mismo escenario en modo JDBC
Entonces la restricción FK fk_visits_pets impediría borrar la mascota salvo que se borren antes las visitas
```

**Parámetros:** `@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.EAGER)` en `Pet.visits` (`Pet.java:55`).

**Confianza:** Media — la anotación es clara. Confirmar si borrar historial de visitas es aceptable como comportamiento de negocio requiere **confirmación de SME**; una clínica real probablemente querría conservar el historial médico incluso después de retirar una ficha de mascota.

---

### RULE-028: No existe soft-delete para ninguna entidad
**Categoría:** Ciclo de vida  
**Prioridad:** P1  
**Fuente:** `src/main/resources/db/h2/schema.sql` (ausencia de columnas de estado/borrado)  
**Explicación:** No hay forma de desactivar, archivar o borrar lógicamente ningún registro —propietarios, mascotas, visitas o veterinarios— ni mediante la aplicación ni a nivel de esquema. Todos los registros, una vez creados, existen para siempre salvo que se borren directamente en base de datos.

**Especificación:**
```
Dada cualquier entidad de dominio del sistema
Cuando se necesita una operación de borrado
Entonces no existe endpoint HTTP "delete" en ningún controlador
Y no existe columna "active", "deleted" o "archived" en ninguna tabla
Y un borrado directo en BD de un Owner sería bloqueado por la restricción FK fk_pets_owners
```

**Confianza:** Alta; la ausencia se confirma por inspección de esquema y controladores.

---

### RULE-029: Sin bloqueo optimista ni protección contra edición concurrente
**Categoría:** Ciclo de vida  
**Prioridad:** P1  
**Fuente:** Todos los ficheros de modelo (ausencia de `@Version`, ausencia de columna `version` en el esquema)  
**Explicación:** Dos usuarios pueden editar simultáneamente el mismo propietario, mascota o veterinario; los cambios del último escritor sobrescriben silenciosamente los del primero, sin detección de conflicto.

**Especificación:**
```
Dado que User A carga Owner{id=1, telephone="6085551023"} en T=0
Y User B carga Owner{id=1, telephone="6085551023"} en T=1
Cuando User A guarda telephone="6085559999" en T=2
Y User B guarda telephone="6085557777" en T=3
Entonces el guardado de User B tiene éxito y sobrescribe el cambio de User A
Y el cambio de User A se pierde permanentemente; no hay OptimisticLockException
```

**Confianza:** Alta, ausencia confirmada.

---

## DEFECTOS SOSPECHADOS (bugs preexistentes que requieren validación de SME)

| ID | Regla | Defecto | Severidad |
|----|-------|---------|-----------|
| RULE-005 | Nombre de mascota único por propietario | La comprobación de duplicado se omite al actualizar; se permiten dos mascotas con el mismo nombre mediante edición | Media |
| RULE-006 | Tipo de mascota obligatorio | El tipo no se revalida al actualizar; type null causa NPE en JDBC o error de BD en JPA en lugar de error de formulario | **Alta** |
| RULE-009 | Fecha de visita por defecto hoy | Se aceptan fechas futuras sin error y fechas anteriores al nacimiento de la mascota | Media |
| RULE-015 | Búsqueda de propietario por prefijo | La sensibilidad a mayúsculas difiere entre H2 y los perfiles MySQL/PostgreSQL | Media |
| RULE-016 | Búsqueda vacía devuelve todos | Sin paginación ni límite de filas; full table scan ante búsqueda en blanco | Media |
| RULE-024 | Visita de una sola escritura | La inmutabilidad solo se fuerza en JDBC; JPA permitiría actualización silenciosa | Media |
| RULE-030 | Inconsistencia de formato de fecha | El formato de entrada (`yyyy/MM/dd`) difiere del formato de visualización (`yyyy-MM-dd`) | Baja |
| RULE-003 | Campos obligatorios del propietario | Sin `@Size(max)`; nombres > 30 caracteres pasan validación pero fallan por longitud de columna en BD | Media |

---

## REGLAS QUE REQUIEREN CONFIRMACIÓN DE SME

Las siguientes reglas tienen confianza inferior a Alta o contienen preguntas de comportamiento que solo puede responder un experto de dominio. Toda regla P0 aquí es un **bloqueante** para iniciar una reescritura.

| Regla | Pregunta | Riesgo si es incorrecto |
|-------|----------|-------------------------|
| **RULE-005** | ¿Es intencional que la comprobación de nombres duplicados de mascota se omita al actualizar? ¿O es un bug que nunca se detectó? | Medio — dos mascotas con el mismo nombre bajo un propietario causan confusión en UI y posibles problemas de integridad de datos |
| **RULE-006** | ¿Debe revalidarse el tipo de mascota al actualizar, es decir, impedir borrar el tipo mediante edición? | **Alto** — actualmente causa NPE en modo JDBC y violación de constraint en JPA |
| **RULE-002** | ¿Es suficiente un máximo de 10 dígitos para el mercado objetivo? ¿Debe haber un mínimo, por ejemplo 7 dígitos? ¿Deben soportarse números internacionales? | Medio — afecta a cualquier clínica con clientes internacionales |
| **RULE-015** | ¿La búsqueda por apellido de propietario debe ser case-insensitive en todos los backends de base de datos y no solo en H2? Si es así, hay que especificar colación en scripts de migración para MySQL/PostgreSQL | Medio — comportamiento distinto en producción frente a desarrollo |
| **RULE-020** | ¿Cuál es la política prevista para invalidar la caché de veterinarios? ¿Debe expirar por TTL o es aceptable el comportamiento de "reiniciar para ver nuevos veterinarios"? | Medio — afecta al SLA operativo de cualquier clínica que añada o elimine veterinarios |
| **RULE-026** | ¿Borrar todas las mascotas, y sus visitas, cuando se borra un propietario es el comportamiento de negocio correcto? ¿Debe existir un paso de archivado? | **Alto** — pérdida permanente de historiales médicos |
| **RULE-027** | ¿Es aceptable borrar todo el historial de visitas cuando se borra una mascota? Una clínica real podría querer conservar el historial médico incluso después de retirar la mascota | **Alto** — pérdida permanente de historiales médicos |
| **RULE-024** | ¿Las visitas deberían poder editarse o borrarse alguna vez? El comportamiento actual de "solo escritura" puede reflejar una intención regulatoria de trazabilidad o ser simplemente una funcionalidad no implementada | Medio — condiciona todo el modelo de datos de visitas |
| **RULE-025** | ¿Cómo se añaden nuevos veterinarios y especialidades en producción: inserts directos en BD, una herramienta de administración separada o una UI admin planificada pero no implementada? `Vet.addSpecialty()` existe pero nunca se llama | Medio — afecta al runbook de despliegue |
| **RULE-016** | ¿La búsqueda de propietarios debería tener un tope máximo de resultados o paginación para proteger frente a full-table scans? | Medio — riesgo de escalabilidad con volumen |
