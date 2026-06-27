# GRUPO5-DATAVISUALIZATION

## Tema
Análisis de brechas socioeconómicas y evolución temporal de ingresos y gastos en hogares peruanos durante 2024.

## Fuente
ENAHO 2024 - Módulo 34 Sumaria, INEI.

## Unidad de análisis
Una fila representa un hogar encuestado.

## Estructura
- Data/original: dataset original.
- Data/limpio: dataset limpio preliminar.
- notebooks: perfilado y limpieza.
- docs: propuesta, diccionario y bitácora.

## Entrega 1
Incluye propuesta del proyecto, pregunta analítica, usuario objetivo, fuente, hipótesis y justificación.

## Entrega 2
Incluye notebook de perfilado y limpieza, dataset limpio, diccionario de datos y bitácora de transformaciones.

## Entrega 3
Arquitectura y Modelado de Datos para Tableau. Incluye un notebook de modelado reproducible, el rediseño de los datos en Esquema Estrella, un reporte de benchmarking matemático (Prueba de estrés de RAM y simulación de escalabilidad a 5 años) comparando 3 arquitecturas (Tabla Plana, Estrella y Copo de Nieve), y los archivos CSV optimizados para su carga nativa en Tableau.

## Entrega 4
Segmentación y Cálculos Analíticos. Incluye un notebook dedicado al cálculo de la métrica derivada `TASA_AHORRO` y la generación de un clúster financiero de 4 perfiles en una nueva dimensión (`dim_segmento`). Se documentaron las reglas de negocio, se corrigieron bugs analíticos sobre participaciones proporcionales de gasto (`_PCT`), y se garantizó la integridad referencial y de tipos para la conexión final a Tableau sin reprocesamiento manual.

## Entrega 5
Visualización Exploratoria y Dashboard Alpha. Se adoptó el enfoque de "Problema Único Crítico" centrado en la asfixia alimentaria de los hogares en Déficit Crítico operativo (`ID_SEGMENTO = 4`). Incluye el documento técnico formal (`docs/Entrega_5_Visualizacion_Exploratoria.md`) con la matriz oficial de selección de 4 gráficos (Composición 100%, Ranking Departamental Horizontal, Tendencia Estacional Mensual y Distribución Boxplot) y la justificación empírica de descarte de 2 gráficos preliminares. Además, presenta 4 insights redactados bajo jerarquía institucional MIDIS (Foco -> Driver -> Acción de Gobierno) y la estructura del prototipo navegable Alpha 1280x720.