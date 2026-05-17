# Entrega 3: Reporte de Preprocesamiento y Decisión de Modelo de Datos

## 1. Preprocesamiento para el Modelado
Para esta entrega, el objetivo fue preparar la arquitectura de datos que será consumida directamente por Tableau. Se partió del archivo `Sumaria-2024_limpio.csv` (33,691 registros y 26 variables, incluyendo métricas derivadas).

### Pasos ejecutados de forma reproducible:
1. **Generación de Claves Primarias:** Dado que en la reducción de dimensionalidad (Entrega 2) se eliminaron las llaves originales del INEI (CONGLOME, VIVIENDA, HOGAR), se generó una clave primaria secuencial subrogada `ID_HOGAR` (del 1 al 33,691) para garantizar que cada registro sea único en la tabla principal y optimizar la velocidad computacional en Tableau.
2. **Generación de Claves para Dimensiones:** Se crearon claves foráneas como `ID_POBREZA` (secuencial) e `ID_GEOGRAFIA` (secuencial) cruzando combinaciones únicas de atributos categóricos, garantizando integridad referencial.
3. **Formateo Estructural de Identificadores (Casting):** Las herramientas como Tableau dependen de tipos de datos estrictos. Se forzó el tipado String para el `UBIGEO` aplicando la función `zfill(6)` durante la carga. Esto solucionó un error crítico de ingesta donde códigos geográficos como Amazonas ("010101") perdían su cero a la izquierda.
4. **Validación de Integridad:** Se validó de forma automatizada (mediante *asserts* en Python) que hacer un *inner join* entre la Tabla de Hechos y las Tablas de Dimensión diera como resultado exactamente las mismas 33,691 filas iniciales, asegurando cero pérdida de datos.

---

## 2. Opciones de Modelo Consideradas

Como las herramientas de visualización de datos como Tableau requieren estructuras altamente eficientes para procesar millones de registros, se compararon dos modelos clásicos de Data Warehousing:

### Opción 1: Modelo de Tabla Plana (Flat Table) - Modelo Base
Es una única tabla desnormalizada ("sábana de datos") donde toda la información se concentra en cada registro.
*   **Funcionamiento:** Similar a un archivo Excel tradicional. Si hay 10,000 hogares en "Lima Metropolitana", el texto se repite 10,000 veces.
*   **Ventaja:** Fácil lectura humana directa sin necesidad de realizar cruces de tablas.
*   **Desventaja (Por qué se descartó):** Altísima redundancia. Demostramos empíricamente que proyectar datos históricos en este formato hace que el archivo se vuelva insosteniblemente pesado en memoria.

### Opción 2: Esquema Estrella (Star Schema) - Modelo Propuesto ⭐
Un modelo normalizado donde el dataset se divide en una tabla central rodeada de dimensiones lógicas (diccionarios):
*   **Tabla de Hechos (`fact_hogares`):** Guarda estrictamente números puros (Gastos, Ingresos, Brechas, IDs) y las llaves foráneas. Cero texto descriptivo.
*   **Las Dimensiones:** Son diccionarios para Geografía (`dim_geografia`), Tiempo (`dim_tiempo`) y Pobreza (`dim_pobreza`).
*   **Ventaja:** Elimina la redundancia ahorrando memoria masivamente (33%). Además, permite que Tableau renderice visualizaciones a máxima velocidad porque solo requiere un salto directo (*1 Join*) desde los Hechos a cualquier Dimensión.

### Opción 3: Esquema Copo de Nieve (Snowflake Schema)
Es una variación de la Estrella llevada a una normalización extrema (3NF), donde las ramas se rompen en pedazos más pequeños:
*   **Funcionamiento:** La dimensión geográfica se disgrega. `dim_geografia_snow` elimina el texto del departamento y lo vincula a una nueva tabla aislada `dim_departamento` mediante un `ID_DEP`.
*   **Desventaja (Por qué se descartó):** Aunque logra una compresión fraccionalmente mejor, obliga al motor de Tableau a realizar múltiples saltos en cascada (*Joins* encadenados: Hechos -> Geografía -> Departamento). Este costo topológico ralentiza los cruces sin justificar el minúsculo ahorro de RAM.

---

## 3. Pruebas de Benchmarking Analítico

Para no depender de preferencias técnicas, se ejecutó un script en Python que calculó matemáticamente el peso en Memoria RAM (Sparsity) y el Costo Topológico de cada arquitectura sobre nuestros 33,691 registros:

| Métrica Evaluada (Evidencia) | Alternativa Base (Tabla Plana) | Opción 1 (Esquema Estrella) | Opción 2 (Copo de Nieve) | Veredicto Empírico |
| :--- | :--- | :--- | :--- | :--- |
| **Memoria RAM (MB)** | 12.15 MB | **8.15 MB (-32.88%)** | **8.14 MB (-32.98%)** | Ambos esquemas relacionales reducen la redundancia categórica en casi un 33%. El Copo de Nieve ahorra marginalmente (0.01 MB). |
| **Proyección a 5 Años (MB)** | 60.73 MB | **40.03 MB (-34.08%)** | **40.01 MB (-34.11%)** | Al simular 5 años históricos, la brecha absoluta de ahorro sube a más de 20 MB, ya que las dimensiones estrella permanecen estáticas. |
| **Costo Topológico (Saltos)** | Bajo (0 Joins) | **Moderado (1 Join directo)** | Alto (2 Joins en cascada) | El Copo de Nieve exige un Join adicional (Geografía -> Departamento), degradando la velocidad de lectura en Tableau. |

---

## 4. Definición del Modelo Seleccionado

> **Decisión:** El modelo seleccionado para alimentar el Dashboard de la Entrega 4 es el **Opción 1: Esquema Estrella (Star Schema)**.

### Justificación Basada en Evidencia:
A diferencia del enfoque tradicional, hemos basado la decisión en mediciones exactas extraídas de Python (`benchmarking_resultados.csv`):
1. **Prueba de Escalabilidad:** La Tabla Plana se descartó porque demostramos empíricamente su fragilidad histórica. Al simular la inyección de 5 encuestas anuales (2020-2024), la redundancia de texto (ej. repetir "Lima Metropolitana" miles de veces) provoca que la Tabla Plana colapse consumiendo **60.73 MB** de memoria RAM. Por el contrario, el Esquema Estrella mantiene estáticas sus dimensiones geográficas y de pobreza, limitando el consumo a **40.03 MB** (un ahorro proyectado del 34.08%).
2. **Costo Topológico:** El Copo de Nieve logró comprimir la memoria en proporciones casi idénticas a la Estrella (solo ganamos 0.02 MB extra). Sin embargo, nos penaliza con un salto de *Join* adicional en cascada. *Ejemplo práctico:* Si en Tableau el usuario quiere filtrar los gastos por "Amazonas", en el Esquema Estrella el sistema viaja directo de la Tabla de Hechos a la de Geografía (1 salto). En el Copo de Nieve, tiene que viajar de los Hechos a la Geografía, y de ahí al Departamento (2 saltos). Esta cadena de cruces haría que los mapas departamentales en Tableau se rendericen mucho más lento.

Por lo tanto, la evidencia dicta que el **Esquema Estrella es el punto de equilibrio óptimo** entre máxima compresión de memoria para datos históricos (ahorro del 34.08% a 5 años) y velocidad de consulta directa (1 Join).
