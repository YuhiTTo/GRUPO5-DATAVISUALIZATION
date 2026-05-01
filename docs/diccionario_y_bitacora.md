# Diccionario de Datos y Bitácora de Limpieza - ENAHO Sumaria 2024

## 1. Diccionario de Datos (18 Variables Seleccionadas)

| Variable | Tipo | Descripción | Tratamiento en Limpieza |
|---|---|---|---|
| **MES** | String | Mes de ejecución de la encuesta (01-12) | Se aseguró formato String de 2 dígitos (padding con ceros a la izquierda). |
| **UBIGEO** | String | Código de ubicación geográfica departamental, provincial y distrital. | Se aseguró formato String de 6 dígitos (padding con ceros a la izquierda). Vital para mapas en Tableau. |
| **DOMINIO** | Categoría (String) | Dominio geográfico. | Se tradujo de Integer (1-8) a texto (Costa Norte, Sierra Centro, Lima Metropolitana, etc.). |
| **ESTRATO** | Categoría (String) | Estrato demográfico por tamaño de población. | Se tradujo de Integer (1-8) a texto descriptivo. |
| **POBREZA** | Categoría (String) | Condición de pobreza monetaria del hogar. | Se tradujo de Integer (1-3) a texto (Pobre Extremo, Pobre No Extremo, No Pobre). |
| **POBREZAV** | Categoría (String) | Condición de pobreza y vulnerabilidad. | Se tradujo de Integer (1-4) a texto. |
| **INGHOG2D** | Float | Ingreso neto total del hogar en soles. | Conservado como número. Se filtraron valores atípicos (outliers) mediante IQR. |
| **GASHOG2D** | Float | Gasto total bruto del hogar en soles. | Conservado como número. |
| **MIEPERHO** | Integer | Total de miembros del hogar. | Conservado como número. |
| **GRU11HD** | Float | Gasto en Alimentos (Grupo 1) | Conservado como número. |
| **GRU21HD** | Float | Gasto en Vestido y calzado (Grupo 2) | Conservado como número. |
| **GRU31HD** | Float | Gasto en Vivienda, combustible y luz (Grupo 3) | Conservado como número. |
| **GRU41HD** | Float | Gasto en Muebles y enseres (Grupo 4) | Conservado como número. |
| **GRU51HD** | Float | Gasto en Salud y médicos (Grupo 5) | Conservado como número. |
| **GRU61HD** | Float | Gasto en Transportes y comunicaciones (Grupo 6) | Conservado como número. |
| **GRU71HD** | Float | Gasto en Esparcimiento y enseñanza (Grupo 7) | Conservado como número. |
| **GRU81HD** | Float | Gasto en Otros bienes y servicios (Grupo 8) | Conservado como número. |
| **FACTOR07** | Float | Factor de expansión poblacional. | Conservado como número para su uso como ponderador en Tableau. |

---

## 2. Bitácora de Transformación

* **Detección de Codificación:** Se leyó el dataset original (`Sumaria-2024.csv`) usando codificación `latin1` para evitar la corrupción de caracteres especiales en las cabeceras.
* **Reducción de Dimensionalidad:** Se eliminaron las columnas innecesarias del módulo original, reduciendo el dataset estrictamente a las 18 variables arriba listadas.
* **Conversión de Identificadores (UBIGEO y MES):** La columna `UBIGEO` se convirtió a String forzando un padding con ceros a la izquierda mediante el uso de la función `zfill(6)`. Esto soluciona que Tableau no lea los UBIGEos que inician con '0' (como Amazonas = 010101) como números enteros. Igual tratamiento se aplicó para `MES` con `zfill(2)`.
* **Traducción de variables (DOMINIO, ESTRATO, POBREZA y POBREZAV):** Se construyeron diccionarios en memoria y se utilizó la función `.map()` de Pandas para traducir los códigos numéricos a texto descriptivo.
* **Manejo de Outliers (2,037 filas eliminadas):** Se detectaron valores atípicos en la variable de ingresos `INGHOG2D` utilizando el método del Rango Intercuartílico (IQR). Por este motivo, **se eliminaron exactamente 2,037 filas** del dataset original (reduciendo de 33,691 a 31,654 registros). Esto fue crucial para no distorsionar los promedios en el dashboard.
* **Exportación y corrección de Encoding (ESTRATO):** Se exportó el dataset limpio bajo el nombre `Sumaria-2024_limpio.csv` forzando el formato de codificación `utf-8-sig` (UTF-8 con BOM). Esta corrección del encoding solucionó el problema en la variable ESTRATO, donde caracteres como "Área" y "más" se mostraban corruptos en Tableau o Excel. Además, se forzó el uso de comillas dobles para variables tipo texto.
