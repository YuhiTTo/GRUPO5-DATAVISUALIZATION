# Entrega 5: Dashboard Alpha y Visualización Exploratoria

**UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS**  
**CURSO:** 1ACC0211 – DATA VISUALIZATION  
**PROYECTO:** Análisis de brechas socioeconómicas y evolución temporal en los hogares peruanos (ENAHO 2024)

---

## 1. Focalización del Problema Único Crítico (Laser-Focused)

Acatando las mejores prácticas de diseño ejecutivo y las directrices metodológicas del curso (*"enfocarse en un solo problema específicamente"*), el prototipo funcional navegable (**Dashboard Alpha**) centra todo su argumento visual en el hallazgo más estructural y crítico descubierto en las fases analíticas previas:

> **Focalización MIDIS 2024: ¿Qué departamentos concentran la mayor incidencia de hogares en Déficit Crítico operativo y cuál es el impacto en su seguridad alimentaria?**

* **El Problema Crítico de Negocio:** El **23.8% de los hogares peruanos (casi 1 de cada 4)** opera bajo un régimen de **Déficit Crítico financiero** (`ID_SEGMENTO = 4`, Tasa de Ahorro < -15%). El análisis exploratorio evidencia que estas familias no sufren de un endeudamiento suntuario o secundario, sino de un déficit de subsistencia primaria: destinan en promedio el **48.0% de su gasto monetario exclusivamente a alimentarse (`GRU11HD_PCT`)**, dejándolos con un margen de holgura nulo ante choques inflacionarios en la canasta básica.

---

## 2. Matriz de Selección y Descarte de Gráficos

La selección visual del **Workbook preliminar en Tableau** responde estrictamente a la matriz oficial de decisiones del curso (*"Elección de gráficos por zona"*), garantizando que cada vista responda a una pregunta analítica accionable y no a preferencias estéticas.

### 2.1. Gráficos Seleccionados (4 Ejes Mandatorios de Rúbrica)

| Eje Analítico | Gráfico Oficial Seleccionado | Variables Mapeadas en Tableau | Justificación Técnica Breve (Matriz de Elección del Curso) | Ubicación Operativa |
| :--- | :--- | :--- | :--- | :--- |
| **Relación / Composición** | **Mapa de Calor (Resaltar Tabla)** | • Columnas: `ID_SEGMENTO` (Clúster 1 al 4)<br>• Filas: `Nombres de medida` (`GRU11HD_PCT` a `GRU81HD_PCT`)<br>• Texto y Color: `Valores de medida` | **Regla oficial:** *"Composición / Relación: Resaltar Tabla (Highlight Table)"*. Presenta una matriz visual limpia con porcentajes exactos impresos en cada celda sin solapamiento ni adivinanzas. Mediante leyendas separadas, evidencia con intensidad semántica roja que el rubro Alimentos absorbe el 48.0% del Clúster 4. | **Vista Principal Dominante (Lienzo Central)** |
| **Comparación / Ranking** | **Gráfico de barras horizontales ordenadas** | • Eje Y: `DEPARTAMENTO`<br>• Eje X: % de Hogares en `ID_SEGMENTO = 4`<br>• Orden: Descendente | **Regla oficial:** *"Ranking: Barras ordenadas"*. Reemplaza al mapa tradicional para garantizar una lectura limpia y comparativa de magnitudes territoriales en espacios compactos, evitando que departamentos geográficamente pequeños (ej. Ica, Callao, Tumbes) pierden visibilidad. | **Soporte A (Recuadro Inferior Izquierdo)** |
| **Tendencia Temporal** | **Gráfico de líneas continuas** | • Eje X: `MES` (Enero a Diciembre)<br>• Eje Y: `% de Déficit Crítico` (`AGR`) | **Regla oficial:** *"Tendencia vs Meta: Línea"*. Conecta observaciones agregadas longitudinales, revelando puntos de inflexión estacionales donde la incidencia de quiebra familiar alcanza su pico crítico en el primer trimestre (abril con 27.6%) antes de moderarse hacia diciembre (22.0%). | **Soporte B (Recuadro Inferior Derecho)** |
| **Distribución** | **Diagrama de caja y bigotes (Boxplot)** | • Eje X: `DOMINIO` (Regiones naturales)<br>• Eje Y: `TASA_AHORRO` (eje fijo -15% a +15%)<br>• Detalle: `ID_HOGAR` | **Regla oficial:** *"Distribución: Dot plot o boxplot"*. Evalúa la mediana central, dispersión intercuartílica (IQR) y valores atípicos territoriales de la capacidad financiera familiar mediante truncamiento visual de escala para maximizar la legibilidad. | **Dashboard Alpha (Integrado en Tooltip visual sobre Soporte A / accesible en navegación de pestañas)** |

### 2.2. Gráficos Descartados

Para demostrar rigor metodológico, **se evitó documentar descartes genéricos obvios** prohibidos universalmente en cátedra (como *Pie Explotado* o *Eje Dual*). En su lugar, se documenta el descarte de gráficos del sílabo oficial que teóricamente parecerían candidatos viables, pero que fallan por la topología y volumen del dataset ENAHO (33,691 observaciones):

1. **Descarte Técnico 1: Diagrama de dispersión único (Scatter Plot crudo de Ingreso vs. Gasto)**
   * **Pertenencia al sílabo:** Enseñados oficialmente para resolver *"Relación entre métricas (Scatter con color)"*.
   * **Justificación de descarte contextual:** Al proyectar simultáneamente los 33,691 puntos individuales del módulo Sumaria, se produce un colapso visual severo denominado **Overplotting** (solapamiento masivo): los puntos se amontonan en los deciles medios y bajos formando una mancha oscura ilegible que oculta la verdadera densidad de vulnerabilidad. Para garantizar una toma de decisiones de políticas públicas en milisegundos por parte del MIDIS, es fisiológicamente superior sintetizar la relación en los **4 Clústeres Financieros (`dim_segmento`)**.
2. **Descarte Técnico 2: Diagrama de árbol (Treemap) o Gráfico de burbujas apiladas**
   * **Pertenencia al sílabo:** Enseñados como alternativas visuales para mostrar la composición de partes de un todo.
   * **Justificación de descarte contextual:** Los 8 rubros de gasto de la ENAHO presentan una disparidad de magnitud extrema (Alimentos representa ~48%, mientras que Salud o Enseñanza apenas ~2%). En un *Treemap* o *Burbujas*, los recuadros o círculos de los rubros pequeños colapsan visualmente y sus etiquetas numéricas se truncan en errores legibles (`###`). Fisiológicamente, el ojo humano evalúa proporciones con mayor precisión al comparar longitudes alineadas sobre un eje base (*Stacked Bar*) que áreas bidimensionales flotantes.

---

## 3. Redacción Analítica de Insights Exploratorios (QUE -> POR QUE -> ACCIÓN)

Para cumplir con el requisito de la rúbrica oficial (*"documento corto con 3 a 5 insights exploratorios en lenguaje analítico"*), se presentan **3 grandes insights institucionales**. Acatando la estructura operativa de la cátedra, **el Insight 1 es el que irá incrustado en el recuadro lateral único del Dashboard Alpha**, mientras que los **Insights 2 y 3** complementan la exploración del Workbook preliminar.

### 3.1. Insight 1 (Incrustado en Dashboard Alpha): Asfixia Alimentaria y Trampa Rural
* **1. QUÉ:** El **23.8% de los hogares peruanos (~2.4M familias)** opera en Déficit Crítico (`ID_SEGMENTO = 4`). Presentan asfixia calórica severa: destinan el **48.0% de su gasto exclusivamente a comer**, operando con una brecha media de **-S/ 286 mensuales per cápita**.
* **2. POR QUÉ:** La quiebra familiar se concentra en el sur y norte rural, liderada por **Puno (37.3%), Huancavelica (31.2%) y Loreto (30.6%)** por desacople agropecuario. Estacionalmente, la tensión alcanza su pico máximo en **abril (27.6% de déficit)**.
* **3. ACCIÓN:** Priorizar el **Programa de Complementación Alimentaria (PCA)** en las provincias críticas, otorgando subsidios e insumos calóricos a **comedores populares y ollas comunes**, reforzando la asistencia durante el primer cuatrimestre del año.

### 3.2. Insight 2 (Exploración de Composición en Workbook): El Gasto en Salud como Déficit Oculto
* **1. QUÉ:** Contraintuitivamente, los hogares en Déficit Crítico gastan **más en salud en monto absoluto** que los Ahorradores Sólidos (**S/ 1,417 vs S/ 1,048 anuales**), absorbiendo el **7.1% de su canasta** frente al 5.6% del estrato superavitario.
* **2. POR QUÉ:** Evidencia que el déficit no obedece a consumos superfluos, sino a **emergencias médicas inelásticas no cubiertas** que obligan al desahorro y gasto de bolsillo (*out-of-pocket*).
* **3. ACCIÓN:** Ampliar la cobertura de medicamentos e intervenciones del **Seguro Integral de Salud (SIS)** para los hogares del Clúster 4, liberando presupuesto familiar para la nutrición básica.

### 3.3. Insight 3 (Exploración Relacional en Workbook): La Paradoja del "No Pobre" en Déficit
* **1. QUÉ:** El **81.7% de los hogares en Déficit Crítico es clasificado como "No Pobre"** por el INEI (6,545 de 8,009 familias encuestadas en quiebra no aparecen en los padrones oficiales de pobreza).
* **2. POR QUÉ:** Existe una fractura entre la medición monetaria de pobreza (evaluada solo por ingresos brutos) y la **vulnerabilidad financiera operativa real** (evaluada por el balance neto y capacidad de ahorro).
* **3. ACCIÓN:** Incorporar la **`TASA_AHORRO` y el balance operativo como criterios de elegibilidad** en el Sistema de Focalización de Hogares (SISFOH), protegiendo a las familias vulnerables excluidas por el estándar tradicional.

