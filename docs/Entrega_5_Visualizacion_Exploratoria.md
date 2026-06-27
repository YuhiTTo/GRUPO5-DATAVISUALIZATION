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

## 2. Matriz de Selección y Descarte de Gráficos (Catálogo Oficial)

La selección visual del **Workbook preliminar en Tableau** responde estrictamente a la matriz oficial de decisiones del curso (*"Elección de gráficos por zona"*), garantizando que cada vista responda a una pregunta analítica accionable y no a preferencias estéticas.

### 2.1. Gráficos Seleccionados (4 Ejes Mandatorios de Rúbrica)

| Eje Analítico | Gráfico Oficial Seleccionado | Variables Mapeadas en Tableau | Justificación Técnica Breve (Matriz de Elección del Curso) | Ubicación Operativa |
| :--- | :--- | :--- | :--- | :--- |
| **Relación / Composición** | **Gráfico de barras apiladas (Stacked Bar 100%)** | • Eje X: `ID_SEGMENTO` (Clúster 1 al 4)<br>• Eje Y: `GRU11HD_PCT` a `GRU81HD_PCT`<br>• Color: Paleta semántica de rubros | **Regla oficial:** *"Composición: Stacked bar (no pie)"*. Normaliza canastas monetarias heterogéneas al 100%. Evidencia de forma dominante la asfixia estructural del Clúster 4, donde el rubro Alimentos (verde) absorbe casi la mitad del presupuesto. | **Vista Principal Dominante (Lienzo Central)** |
| **Comparación / Ranking** | **Gráfico de barras horizontales ordenadas** | • Eje Y: `DEPARTAMENTO`<br>• Eje X: % de Hogares en `ID_SEGMENTO = 4`<br>• Orden: Descendente | **Regla oficial:** *"Ranking: Barras ordenadas"*. Reemplaza al mapa tradicional para garantizar una lectura limpia y comparativa de magnitudes territoriales en espacios compactos, evitando que departamentos geográficamente pequeños (ej. Ica, Callao, Tumbes) pierden visibilidad. | **Soporte A (Recuadro Inferior Izquierdo)** |
| **Tendencia Temporal** | **Gráfico de líneas continuas** | • Eje X: `MES_NUM` (Meses cronológicos 1-12)<br>• Eje Y: Promedio de `BRECHA_PERCAPITA`<br>• Color: `ID_SEGMENTO` | **Regla oficial:** *"Tendencia vs Meta: Línea"*. Conecta observaciones agregadas longitudinales, revelando puntos de inflexión estacionales poblacionales y caídas abruptas de holgura operativa. | **Soporte B (Recuadro Inferior Derecho)** |
| **Distribución** | **Diagrama de caja y bigotes (Boxplot)** | • Eje X: `DOMINIO` (Regiones naturales)<br>• Eje Y: `TASA_AHORRO`<br>• Detalle: `ID_HOGAR` | **Regla oficial:** *"Distribución: Dot plot o boxplot"*. Evalúa la mediana central, dispersión intercuartílica (IQR) y valores atípicos territoriales de la capacidad financiera familiar. | **Dashboard Alpha (Integrado en Tooltip visual sobre Soporte A / accesible en navegación de pestañas)** |

### 2.2. Gráficos Descartados (Exclusivamente del sílabo oficial de 24 gráficos)

Para demostrar rigor metodológico, **se evitó documentar descartes genéricos obvios** prohibidos universalmente en cátedra (como *Pie Explotado* o *Eje Dual*). En su lugar, se documenta el descarte de gráficos del sílabo oficial que teóricamente parecerían candidatos viables, pero que fallan por la topología y volumen del dataset ENAHO (33,691 observaciones):

1. **Descarte Técnico 1: Diagrama de dispersión único (Scatter Plot crudo de Ingreso vs. Gasto)**
   * **Pertenencia al sílabo:** Enseñados oficialmente para resolver *"Relación entre métricas (Scatter con color)"*.
   * **Justificación de descarte contextual:** Al proyectar simultáneamente los 33,691 puntos individuales del módulo Sumaria, se produce un colapso visual severo denominado **Overplotting** (solapamiento masivo): los puntos se amontonan en los deciles medios y bajos formando una mancha oscura ilegible que oculta la verdadera densidad de vulnerabilidad. Para garantizar una toma de decisiones de políticas públicas en milisegundos por parte del MIDIS, es fisiológicamente superior sintetizar la relación en los **4 Clústeres Financieros (`dim_segmento`)**.
2. **Descarte Técnico 2: Diagrama de árbol (Treemap) o Gráfico de burbujas apiladas**
   * **Pertenencia al sílabo:** Enseñados como alternativas visuales para mostrar la composición de partes de un todo.
   * **Justificación de descarte contextual:** Los 8 rubros de gasto de la ENAHO presentan una disparidad de magnitud extrema (Alimentos representa ~48%, mientras que Salud o Enseñanza apenas ~2%). En un *Treemap* o *Burbujas*, los recuadros o círculos de los rubros pequeños colapsan visualmente y sus etiquetas numéricas se truncan en errores legibles (`###`). Fisiológicamente, el ojo humano evalúa proporciones con mayor precisión al comparar longitudes alineadas sobre un eje base (*Stacked Bar*) que áreas bidimensionales flotantes.

---

## 3. Redacción Analítica de Insights Exploratorios (Foco -> Driver -> Acción)

Para cumplir con el requisito de la rúbrica oficial (*"documento corto con 3 a 5 insights exploratorios en lenguaje analítico"*), se presentan **3 grandes insights institucionales**. Acatando la estructura operativa de la cátedra, **el Insight 1 es el que irá incrustado en el recuadro lateral único del Dashboard Alpha**, mientras que los **Insights 2 y 3** complementan la exploración del Workbook preliminar.

### 3.1. Insight 1 (Incrustado en Dashboard Alpha): Asfixia Alimentaria y Trampa Rural del Déficit Crítico
* **1 - FOCO (El problema operativo dominante):**  
  El **23.8% de los hogares peruanos (~2.4 millones de familias ponderadas)** opera en Déficit Crítico operativo permanente (`ID_SEGMENTO = 4`). Su canasta básica presenta asfixia calórica severa: destinan el **48.0% de su efectivo exclusivamente a comprar alimentos (`GRU11HD_PCT` en Vista Principal)**, operando con una brecha media de **-S/ 286 mensuales per cápita**.
* **2 - DRIVER (Explicadores espaciales y temporales):**  
  La trampa financiera se concentra territorialmente en el sur y norte rural, liderado por **Puno (38.3% en Déficit Crítico), Loreto (30.5%) y Cajamarca (26.2%)** en el Ranking del *Soporte A*, debido al desacople entre ingresos agropecuarios y costos fijos productivos. Asimismo, la serie longitudinal (*Soporte B*) revela una oscilación anual de 3.9 pp en la incidencia de déficit (peor mes en marzo con 25.8% vs mejor mes en diciembre con 21.9%) y una tensión financiera máxima en enero (-10.3% de brecha).
* **3 - ACCIÓN (Sugerencia de mitigación MIDIS):**  
  Priorizar la focalización del **Programa de Complementación Alimentaria (PCA)** en las provincias críticas del Ranking (*Soporte A*), otorgando subsidios económicos e insumos directos a **comedores populares y ollas comunes** para garantizar raciones de alimentos calóricos a las familias del Clúster 4. Complementariamente, **reforzar la asistencia temporal a inicios de año** para amortiguar la tensión financiera del primer trimestre (*Soporte B*).

### 3.2. Insight 2 (Exploración de Composición en Workbook): El Gasto en Salud como Señal de Déficit Oculto
* **1 - FOCO:** De forma contraintuitiva, los hogares en Déficit Crítico (`ID_SEGMENTO = 4`) gastan **más en salud en términos absolutos que los Ahorradores Sólidos (`ID_SEGMENTO = 1`)**: destinan **S/ 1,417 vs S/ 1,048 anuales**. En peso relativo, la salud absorbe el **7.1% de su canasta monetaria frente al 5.6%** de los sectores con superávit (`GRU81HD_PCT`).
* **2 - DRIVER:** Este comportamiento revela que la caída en déficit crítico no obedece a consumos superfluos o suntuarios, sino a eventos médicos inelásticos y emergencias de salud no cubiertas que obligan a las familias vulnerables a descapitalizarse mediante gasto de bolsillo (*out-of-pocket*).
* **3 - ACCIÓN:** Ampliar la cobertura financiera, de medicamentos e intervenciones del **Seguro Integral de Salud (SIS)** con focalización prioritaria en los hogares del Clúster 4, liberando este gasto cautivo para que el presupuesto familiar pueda redirigirse a la nutrición básica.

### 3.3. Insight 3 (Exploración Relacional en Workbook): La Paradoja del "No Pobre" en Déficit Crítico
* **1 - FOCO:** El **81.7% de los hogares en Déficit Crítico (`ID_SEGMENTO = 4`) es clasificado oficialmente como "No Pobre"** según la metodología monetaria tradicional del INEI (6,545 de 8,009 hogares encuestados en asfixia severa no aparecen en los padrones de pobreza oficial).
* **2 - DRIVER:** Existe una fractura estructural entre la medición oficial de pobreza (evaluada únicamente por umbrales de ingreso bruto per cápita) y la vulnerabilidad financiera operativa real (evaluada por el balance neto de ingresos menos gastos y la capacidad de ahorro familiar).
* **3 - ACCIÓN:** Incorporar la variable **`TASA_AHORRO` y el balance operativo de los hogares como criterios complementarios de elegibilidad** en el Sistema de Focalización de Hogares (SISFOH) del MIDIS, evitando que casi 1 de cada 4 familias "no pobres" que vive en asfixia permanente quede excluida de las redes de protección del Estado.

---

## 4. Estructura Navegable del Dashboard Alpha (Plantilla 1280 x 720)

El prototipo funcional en Tableau replica fielmente la jerarquía visual operativa enseñada por la cátedra:

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: ¿Dónde se concentra la trampa del Déficit Crítico familiar y cuál es su asfixia alimentaria? |
|          Periodo: 2024 enero a diciembre | Filtros: [Dominio] [Estrato] [Clúster] [Trimestre/Mes]|
+------------------------+------------------------+------------------------+------------------------+
|  KPI 1: HOGARES DÉFICIT|  KPI 2: BRECHA MEDIA   |  KPI 3: PESO ALIMENTOS |  KPI 4: AHORRO PAÍS    |
|  23.8%                 |  -S/ 286 / mes         |  48.0% / canasta       |  11.2%                 |
|  Alerta crítica (>20%) |  Media poblacional     |  Inelasticidad severa  |  Mediana nacional      |
+------------------------+------------------------+------------------------+------------------------+
|                                                  | PANEL DE INSIGHTS (Barra Lateral Derecha)       |
|  VISTA PRINCIPAL DOMINANTE                       | Donde priorizar capacidad presupuestaria MIDIS  |
|  Gráfico de Barras Apiladas 100%                 |                                                 |
|  • Eje X: Clústeres Financieros (Segmentos 1 al 4) | 1 - FOCO: Déficit alimentario severo            |
|  • Eje Y: % de participación por rubro (1 al 8)  | El Clúster 4 destina 48.0% a comer; nulo margen |
|                                                  | ante shocks de precios agrícolas.               |
|  Dominancia visual: Resalta en verde el enorme   |                                                 |
|  bloque alimentario del Clúster 4.               | 2 - DRIVER: Sur y Norte rural                   |
|                                                  | Puno supera el 38% y Loreto el 30% de déficit   |
+-------------------------+------------------------+ por desacople de ingresos agropecuarios.        |
|  SOPORTE A (Driver)     | SOPORTE B (Excepción)  |                                                 |
|  Ranking Departamentos  | Tendencia Estacional   | 3 - ACCION: Subsidios e insumos directos PCA    |
|  Barras Horizontales    | Líneas Continuas       | Focalizar Programa de Complementación Aliment.  |
|  (+ Tooltip visual:     | Serie mensual (MES 1-12) | (PCA) en comedores populares y ollas comunes.   |
|   Boxplot Distribución) |                        |                                                 |
+-------------------------+------------------------+-------------------------------------------------+
|  FOOTER: Fuente: INEI (ENAHO 2024 Sumaria) | Expansión poblacional automática mediante FACTOR07   |
+---------------------------------------------------------------------------------------------------+
```

### Flujo de Interacción Declarado:
1. **Acción de Filtro Principal:** Al hacer clic sobre cualquier barra departamental del **Soporte A** (ej. *Cajamarca*), el motor relacional de Tableau filtra simultáneamente la Vista Principal Dominante, el Soporte B y las 4 tarjetas KPI superiores, recalculando los porcentajes ponderados por `FACTOR07` en tiempo real.
2. **Exploración de Distribución (Tooltip / Pestaña Boxplot):** Al posicionar el cursor sobre cualquier barra departamental del **Soporte A**, se despliega un *Tooltip visual interactivo* que incrusta el **Diagrama de caja y bigotes (Boxplot)** mostrando la dispersión y mediana de la `TASA_AHORRO` de los hogares de dicho departamento. Asimismo, esta vista de distribución está accesible a pantalla completa en las pestañas de navegación del Workbook preliminar.

