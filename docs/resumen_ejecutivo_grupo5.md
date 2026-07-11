# Resumen Ejecutivo

## Proyecto

**Análisis de brechas socioeconómicas y evolución temporal de ingresos y gastos en los hogares peruanos durante el 2024**

## Problema identificado

Las cifras macroeconómicas y la clasificación de pobreza monetaria no siempre muestran toda la presión financiera que enfrentan los hogares. Un hogar puede no estar clasificado como pobre y, aun así, presentar una brecha negativa entre el ingreso y el gasto registrados, una capacidad de ahorro nula o una alta exposición frente a incrementos en el costo de los alimentos.

Esta limitación dificulta la identificación de territorios, periodos y perfiles de hogares que requieren mayor atención. Por ello, el proyecto analiza la brecha entre ingresos y gastos como una dimensión complementaria de vulnerabilidad económica para apoyar decisiones de focalización del MIDIS.

## Objetivo

Identificar qué perfiles de hogares peruanos presentan las mayores brechas entre ingreso y gasto durante 2024, analizar cómo se distribuyen según territorio, estrato, condición de pobreza y mes de entrevista, y presentar los resultados en un dashboard para apoyar decisiones de focalización social.

## Fuente de datos y alcance

El análisis utiliza la **Encuesta Nacional de Hogares 2024, Módulo 34: Sumaria**, publicada por el Instituto Nacional de Estadística e Informática (INEI).

- **Unidad de análisis:** hogar.
- **Registros analizados:** 33,691 hogares.
- **Cobertura:** nacional.
- **Periodo:** enero a diciembre de 2024.
- **Principales dimensiones:** departamento, dominio geográfico, estrato, condición de pobreza y mes de entrevista.
- **Principales métricas:** ingreso, gasto, brecha ingreso-gasto, brecha per cápita, tasa de ahorro y composición porcentual del gasto.

## Metodología

El proyecto se desarrolló mediante un pipeline reproducible en Python y Tableau:

1. Perfilado y validación de la base original.
2. Homologación de tipos, códigos geográficos y categorías.
3. Tratamiento documentado de valores atípicos en ingresos y gastos.
4. Construcción de métricas derivadas: brecha ingreso-gasto, brecha per cápita y tasa de ahorro.
5. Segmentación financiera de los hogares según la tasa de ahorro.
6. Modelado de datos mediante un esquema estrella.
7. Preparación de fuentes finales para Tableau.
8. Aplicación de PCA y evaluación de t-SNE como componente avanzado.
9. Construcción de vistas de comparación territorial, análisis temporal agregado, composición del gasto y PCA dentro del dashboard.

La segmentación financiera considera cuatro perfiles:

- **Ahorrador sólido:** tasa de ahorro mayor o igual a 15%.
- **Equilibrio o supervivencia:** tasa de ahorro entre 0% y 15%.
- **Déficit leve:** tasa de ahorro entre -15% y 0%.
- **Déficit crítico:** tasa de ahorro menor a -15%.

## Principales hallazgos

### 1. Una proporción relevante de hogares se encuentra en déficit crítico

En la base transformada y ponderada, aproximadamente **24.54% de los hogares** se ubica en el segmento de déficit crítico. Esto equivale a cerca de **2.54 millones de hogares expandidos**. Esta cifra debe interpretarse como resultado de la base tratada y ponderada, no como cifra cruda oficial de la ENAHO.

### 2. La vulnerabilidad presenta concentración territorial

La vista transversal del dashboard muestra que **Puno (37.3%)**, **Huancavelica (31.2%)** y **Loreto (30.6%)** presentan algunas de las mayores incidencias de déficit crítico. Esto evidencia que la presión financiera no se distribuye de forma homogénea y que el promedio nacional oculta diferencias territoriales importantes.

### 3. Existen diferencias según el mes de entrevista

La vista temporal agregada muestra variaciones mensuales en la incidencia del déficit crítico. El mayor valor observado aparece en **abril (27.6%)**, mientras que el menor se observa en **diciembre (22.0%)**. Este resultado compara hogares entrevistados en distintos meses y no debe interpretarse como seguimiento de las mismas familias a lo largo del año.

### 4. La alimentación concentra una parte importante del gasto, pero no diferencia por sí sola los segmentos

En el segmento de déficit crítico, los alimentos representan aproximadamente **48.0%** del gasto monetario. Sin embargo, este porcentaje también es elevado en otros segmentos, por lo que la diferencia principal entre perfiles no está en una canasta completamente distinta, sino en el margen disponible entre ingresos y gastos.

### 5. La pobreza monetaria y la vulnerabilidad financiera no son equivalentes

Una proporción importante de los hogares clasificados en déficit crítico aparece como no pobre bajo la clasificación monetaria tradicional. Esto sugiere que la pobreza monetaria y el déficit operativo capturan dimensiones distintas y complementarias de la vulnerabilidad económica.

### 6. PCA y t-SNE no separan claramente los segmentos financieros

El PCA aplicado a la composición porcentual de ocho rubros de gasto muestra que los dos primeros componentes explican **39.31% de la varianza acumulada**. Sin embargo, los segmentos se superponen ampliamente. Esto indica que la composición del gasto, por sí sola, no distingue con claridad la vulnerabilidad financiera. La tasa de ahorro y la brecha ingreso-gasto resultan señales más directas para identificar el estrés económico de los hogares.

## Producto final

El producto final incluye:

- un dashboard en Tableau;
- KPIs nacionales de incidencia, brecha, desahorro y gasto en alimentos;
- una vista transversal de ranking departamental;
- una vista temporal agregada según mes de entrevista;
- una vista de composición porcentual del gasto por segmento;
- una vista PCA para evaluar la separación visual de los segmentos;
- notebooks reproducibles en Python;
- fuentes de datos preparadas para Tableau;
- documentación metodológica y técnica.

## Valor para el usuario objetivo

El dashboard permite a los analistas del MIDIS:

- identificar departamentos con mayor incidencia de déficit crítico;
- comparar vulnerabilidad financiera con clasificación de pobreza;
- analizar diferencias territoriales y mensuales;
- explorar la composición del gasto por segmento;
- complementar los criterios tradicionales de focalización con indicadores de brecha y tasa de ahorro.

## Recomendaciones

1. Considerar la tasa de ahorro y la brecha ingreso-gasto como indicadores complementarios a la clasificación de pobreza monetaria.
2. Priorizar el análisis de departamentos con mayor incidencia ponderada de hogares en déficit crítico.
3. Reforzar el seguimiento de la vulnerabilidad durante los meses en los que se observa mayor incidencia o severidad de la brecha.
4. Utilizar la composición del gasto y el análisis PCA como soporte exploratorio, no como criterio único de clasificación.
5. Mantener diferenciados los resultados crudos, transformados, muestrales y ponderados.

## Limitaciones

- El análisis es exploratorio y no permite establecer relaciones causales.
- La ENAHO 2024 no sigue necesariamente a los mismos hogares durante los doce meses.
- El tratamiento de valores atípicos modifica parcialmente la distribución de los segmentos.
- Los dos primeros componentes del PCA explican una fracción limitada de la varianza total.
- PCA y t-SNE complementan la interpretación, pero no constituyen modelos definitivos de clasificación.
- El dashboard debe utilizarse como herramienta de apoyo y no como sustituto de una evaluación social o administrativa individual.

## Conclusión

El proyecto transforma los datos de la ENAHO 2024 en una herramienta de análisis orientada a la toma de decisiones. Su principal aporte consiste en complementar la pobreza monetaria con una medición de vulnerabilidad basada en el balance entre ingresos y gastos.

Al integrar comparación territorial, análisis temporal agregado, segmentación financiera y reducción de dimensionalidad, el dashboard permite convertir la brecha económica de los hogares en una señal más clara para apoyar la focalización social.
