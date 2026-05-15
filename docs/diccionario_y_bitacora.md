# Diccionario de Datos y Bitácora de Limpieza - ENAHO Sumaria 2024

## 1. Diccionario de Datos (18 Variables Seleccionadas)

| Variable | Tipo | Descripción | Eje Analítico | Justificación Técnica | Tratamiento en Limpieza |
|---|---|---|---|---|---|
| **MES** | String | Mes de ejecución de la encuesta | Temporal | Permite construir la serie temporal mensual para analizar la estacionalidad de la brecha ingreso-gasto. | Se aseguró formato String de 2 dígitos (padding con ceros a la izquierda). |
| **UBIGEO** | String | Código de ubicación geográfica | Geográfico | Permite georreferenciar los hogares en Tableau para construir mapas departamentales. | Se aseguró formato String de 6 dígitos (padding con ceros a la izquierda). Vital para mapas en Tableau. |
| **DOMINIO** | Categoría (String) | Dominio geográfico (Costa Norte, Sierra, Selva, Lima Metropolitana, etc.) | Segmentación geográfica | Permite comparar perfiles de hogares entre las grandes regiones naturales del país. | Se tradujo de Integer (1-8) a texto (Costa Norte, Sierra Centro, Lima Metropolitana, etc.). |
| **ESTRATO** | Categoría (String) | Estrato geográfico según tamaño de población | Segmentación geográfica | Diferencia el ámbito urbano del rural para identificar concentración de perfiles vulnerables. | Se tradujo de Integer (1-8) a texto descriptivo. |
| **POBREZA** | Categoría (String) | Condición de pobreza monetaria del hogar | Clasificación y filtro | Permite validar si los perfiles del clustering coinciden con la clasificación oficial del INEI. | Se tradujo de Integer (1-3) a texto (Pobre Extremo, Pobre No Extremo, No Pobre). |
| **POBREZAV** | Categoría (String) | Condición de pobreza y vulnerabilidad del hogar | Clasificación y filtro | Amplía la clasificación incluyendo hogares vulnerables no pobres, enriqueciendo la segmentación. | Se tradujo de Integer (1-4) a texto. |
| **INGHOG2D** | Float | Ingreso neto total del hogar | Métrica base | Ingreso real disponible del hogar, uno de los dos ejes para calcular la brecha ingreso-gasto. | Conservado como número. Se filtraron valores atípicos (outliers) mediante IQR. |
| **GASHOG2D** | Float | Gasto total bruto del hogar | Métrica base | Junto con INGHOG2D permite construir la brecha ingreso-gasto y determinar qué hogares logran ahorrar. | Conservado como número. |
| **MIEPERHO** | Integer | Total de miembros del hogar | Normalización | Permite calcular ingreso y gasto per cápita, haciendo comparables hogares de distinto tamaño. | Conservado como número. |
| **GRU11HD** | Float | Grupo 1: Alimentos - gasto monetario | Dimensión para PCA/clustering | Representa la proporción del gasto destinada a alimentación dentro de la estructura de consumo del hogar. | Conservado como número. |
| **GRU21HD** | Float | Grupo 2: Vestido y calzado - gasto monetario | Dimensión para PCA/clustering | Captura el gasto en necesidades básicas secundarias para distinguir perfiles de consumo. | Conservado como número. |
| **GRU31HD** | Float | Grupo 3: Vivienda, combustible y electricidad- gasto monetario | Dimensión para PCA/clustering | Refleja el peso de los gastos fijos del hogar en servicios básicos. | Conservado como número. |
| **GRU41HD** | Float | Grupo 4: Muebles, enseres y mantenimiento - gasto monetario | Dimensión para PCA/clustering | Indica la capacidad del hogar para invertir más allá de las necesidades inmediatas. | Conservado como número. |
| **GRU51HD** | Float | Grupo 5: Salud y servicios médicos - gasto monetario | Dimensión para PCA/clustering | Permite detectar perfiles con acceso limitado o nulo a gasto en salud. | Conservado como número. |
| **GRU61HD** | Float | Grupo 6: Transportes y comunicaciones - gasto monetario | Dimensión para PCA/clustering | Refleja el nivel de movilidad e inserción económica del hogar. | Conservado como número. |
| **GRU71HD** | Float | Grupo 7: Esparcimiento, cultura y enseñanza - gasto monetario | Dimensión para PCA/clustering | Captura inversión en capital humano y calidad de vida del hogar. | Conservado como número. |
| **GRU81HD** | Float | Grupo 8: Otros bienes y servicios - gasto monetario | Dimensión para PCA/clustering | Completa el vector de 8 variables numéricas requerido para el componente avanzado PCA/t-SNE. | Conservado como número. |
| **FACTOR07** | Float | Factor de expansión anual | Ponderación estadística | Garantiza que los cálculos representen a la población nacional y no solo a la muestra encuestada. | Conservado como número para su uso como ponderador en Tableau. |

---

## 2. Bitácora de Transformación

* **Detección de Codificación:** Se leyó el dataset original (`Sumaria-2024.csv`) usando codificación `latin1` para evitar la corrupción de caracteres especiales en las cabeceras.
* **Reducción de Dimensionalidad:** Se eliminaron las columnas innecesarias del módulo original, reduciendo el dataset estrictamente a las 18 variables arriba listadas.
* **Conversión de Identificadores (UBIGEO y MES):** La columna `UBIGEO` se convirtió a String forzando un padding con ceros a la izquierda mediante el uso de la función `zfill(6)`. Esto soluciona que Tableau no lea los UBIGEos que inician con '0' (como Amazonas = 010101) como números enteros. Igual tratamiento se aplicó para `MES` con `zfill(2)`.
* **Traducción de variables (DOMINIO, ESTRATO, POBREZA y POBREZAV):** Se construyeron diccionarios en memoria y se utilizó la función `.map()` de Pandas para traducir los códigos numéricos a texto descriptivo.
* **Manejo de Outliers (2,037 filas eliminadas):** Se detectaron valores atípicos en la variable de ingresos `INGHOG2D` utilizando el método del Rango Intercuartílico (IQR). Por este motivo, **se eliminaron exactamente 2,037 filas** del dataset original (reduciendo de 33,691 a 31,654 registros). Esto fue crucial para no distorsionar los promedios en el dashboard.
* **Exportación y corrección de Encoding (ESTRATO):** Se exportó el dataset limpio bajo el nombre `Sumaria-2024_limpio.csv` forzando el formato de codificación `utf-8-sig` (UTF-8 con BOM). Esta corrección del encoding solucionó el problema en la variable ESTRATO, donde caracteres como "Área" y "más" se mostraban corruptos en Tableau o Excel. Además, se forzó el uso de comillas dobles para variables tipo texto.
