# Entrega 6: Trabajo Final Completo — Documento Resumen Ejecutivo y QA

**UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS**
**CURSO:** 1ACC0211 – DATA VISUALIZATION | **NRC:** 18519
**PROYECTO:** Análisis de brechas socioeconómicas y evolución temporal en los hogares peruanos (ENAHO 2024)
**EQUIPO DE TRABAJO (GRUPO 5):**
• Carbajal Robles, Daniel Ivan (U20221B751)
• Manchay Paredes, Lucero Salome (U202216120)
• Mayhua Hinostroza, José Antonio (U202218044)

---

## 1. Resumen Ejecutivo del Proyecto (ENAHO 2024 - MIDIS)

El presente documento consolida la investigación analítica, metodológica y visual desarrollada sobre la Encuesta Nacional de Hogares (**ENAHO 2024**, muestra representativa nacional anual de **33,691 hogares** empadronados por el INEI). El objetivo central del proyecto es proveer al Ministerio de Desarrollo e Inclusión Social (**MIDIS**) un instrumento analítico de decisión pública auditado, reproducible y visualmente claro para optimizar la asignación del gasto fiscal en programas de alivio alimentario y transferencias monetarias focalizadas.

> **Hallazgo Central del Proyecto:**
> El **24.5% de los hogares peruanos a nivel nacional ponderado (y 23.8% muestral)** opera en una condición de **Déficit Crítico Financiero (`ID_SEGMENTO = 4`, criterio `Tasa de Ahorro < -15%`)**, con una tasa agregada de desahorro del **-53.7%** (promedio individual ponderado: -85.1%) y enfrentando una brecha monetaria per cápita media de **-S/ 312 mensuales**. Este déficit estructural no responde a distorsiones en los patrones o hábitos de consumo familiar, sino a una severa rigidez alimentaria (el rubro Alimentos absorbe en promedio el **48.0% del gasto monetario**) combinada con ingresos inelásticos en los dominios rurales y de la Sierra/Selva.

> **Nota metodológica sobre el tratamiento de outliers:** La cifra de 24.54% (ponderada) se calcula **después** de imputar por mediana (agrupada por condición de pobreza) los valores atípicos de `INGHOG2D` (2,037 hogares) y `GASHOG2D` (1,589 hogares), según el método IQR descrito en `01_perfilado_y_limpieza.ipynb`. Sobre los datos crudos de ENAHO, sin este tratamiento, la incidencia ponderada de Déficit Crítico es **22.46%**, y **2,360 hogares** cambian de segmento financiero como resultado directo de la imputación. Este tratamiento es metodológicamente correcto (evita que valores de ingreso/gasto mal reportados distorsionen la segmentación), pero se documenta aquí explícitamente para que la cifra de 24.5% no se presente como un dato crudo de la encuesta, sino como el resultado de la base ya transformada.

---

## 2. Documentación Metodológica de Componentes Avanzados (PCA vs. t-SNE)

Para validar técnicamente las causas de la vulnerabilidad socioeconómica y confirmar si la estructura porcentual de consumo discrimina por sí sola el estrato financiero de una familia, se integró un módulo de **Reducción de Dimensionalidad** sobre los 8 rubros porcentuales de gasto del hogar (`GRU11HD_PCT` a `GRU81HD_PCT`).

### 2.1. Preprocesamiento y Justificación de Estandarización
Antes de proyectar las variables en subespacios de menor dimensión, se aplicó una transformación lineal mediante `StandardScaler(with_mean=True, with_std=True)` sobre las `33,691` observaciones.
* **Justificación Matemática:** El rubro *Alimentos dentro del hogar (`GRU11HD_PCT`)* presenta una media global del `46.2%` con alta varianza absoluta, mientras que rubros marginales como *Salud (`GRU51HD_PCT`)* o *Muebles (`GRU41HD_PCT`)* apenas promedian el `2.4%` y `3.1%` respectivamente. Sin estandarizar, el análisis de componentes principales sería cooptado trivialmente por la escala de Alimentos, enmascarando las dinámicas latentes del consumo secundario.

### 2.2. Análisis y Cargas del Análisis de Componentes Principales (PCA)
El ajuste de `PCA(n_components=8)` arrojó la siguiente distribución de varianza y cargas (*Loadings*) para los primeros ejes latentes:

| Componente Principal | Varianza Explicada | Varianza Acumulada | Carga Dominante (+) | Cargas Dominantes (-) | Interpretación Económica (MIDIS) |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **PC1** | **22.85%** | **22.85%** | `GRU11HD_PCT` (**+0.665**)<br>*(Alimentos hogar)* | `GRU61HD_PCT` (**-0.388**)<br>`GRU21HD_PCT` (**-0.352**)<br>`GRU81HD_PCT` (**-0.323**) | **Eje de subsistencia primaria vs. Bienes/Servicios No Básicos.** Opone directamente la rigidez alimentaria contra la capacidad de gasto en transporte, vestimenta y servicios de calidad de vida. |
| **PC2** | **16.46%** | **39.31%** | `GRU31HD_PCT` (**+0.552**)<br>`GRU51HD_PCT` (**+0.409**)<br>`GRU61HD_PCT` (**+0.179**) | `GRU41HD_PCT` (**-0.429**)<br>`GRU21HD_PCT` (**-0.355**)<br>`GRU11HD_PCT` (**-0.333**) | **Eje de habitabilidad/salud vs. Enseres/Vestimenta.** Diferencia hogares con costos fijos y gastos médicos urgentes (`GRU31HD`, `GRU51HD`) frente a hogares orientados a mantenimiento y vestimenta. |

*(Cifras de varianza y cargas verificadas contra `Data/PCA/pca_varianza.csv` y `pca_loadings.csv`.)*

### 2.3. Benchmarking Cuantitativo: PCA vs. t-SNE
Para evaluar la calidad de las proyecciones en 2D respecto a la separación externa por clústeres financieros (`ID_SEGMENTO` de 1 al 4) y la fidelidad geométrica, se computaron tres métricas formales sobre una muestra estratificada de `3,000 hogares`:

| Técnica Proyectada | Silhouette Score<br>*(Separación de Clústeres)* | Trustworthiness<br>*(Fidelidad local k=10)* | Reproducibilidad<br>*(Pearson Corr Semilla 1 vs 99)* | Ventajas Operativas | Desventajas / Riesgos |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **PCA (2D)** | **-0.0214** | **0.7690** | **1.0000**<br>*(100% Determinístico)* | • **Linealmente interpretable** mediante Cargas (*Loadings*).<br>• Cómputo instantáneo (0.048 s).<br>• Proyección global estable. | • Proyecta combinaciones lineales; puede perder relaciones no lineales complejas. |
| **t-SNE (*Perplexity = 5*)** | -0.0156 | 0.9837 | N/A | • Resalta micro-vecindades locales extremas. | • Muy sensible al ruido; fractura vecindades globales. |
| **t-SNE (*Perplexity = 30*)** | **-0.0183** | **0.9879** | **1.0000**<br>*(Con `init='pca'`)* | • **Máxima preservación de vecindades locales** (98.79% fidelidad topológica en 8D). | • **Caja negra paramétrica:** Carece de *loadings* asignables.<br>• Su implementación en `scikit-learn` usa por defecto **Barnes–Hut** ($O(N \log N)$), no $O(N^2)$. Se optó por una muestra estratificada de 3,000 hogares para mantener la interactividad y comparar contra el mismo subconjunto del Silhouette. |
| **t-SNE (*Perplexity = 50*)** | -0.0191 | 0.9862 | N/A | • Mayor cohesión geométrica que perplexity 5. | • Costo computacional elevado e inercia de clúster difusa. |

### 2.4. Decisión Metodológica Oficial y el Gran "Insight" Analítico

> [!TIP]
> **Decisión de Ingeniería y Política Pública:**
> Se adopta **PCA como la técnica analítica oficial del proyecto** y fuente de coordenadas para el dashboard del MIDIS (`fact_hogares_pca.csv`), empleando **t-SNE (*Perplexity = 30, init='pca'*)** estrictamente como auditoría de fidelidad topológica (*Trustworthiness = 0.9879*). La razón clave es que el diseño de políticas públicas exige **interpretabilidad explicativa exacta**: el MIDIS necesita saber qué variable porcentual específica empuja la coordenada geométrica de un hogar, algo que la transformación lineal del PCA entrega de forma transparente a través de los *Loadings*.

> [!WARNING]
> **Interpretación Empírica del Silhouette Score Cercano a Cero (`-0.0214` en PCA / `-0.0183` en t-SNE):**
> La aparente "baja separación geométrica" entre las nubes de puntos del *Déficit Crítico (`Segmento 4`)* y los hogares en *Equilibrio/Déficit Leve (`Segmento 2 y 3`)* **es el hallazgo de política pública más contundente del proyecto**:
> Aporta evidencia topológica robusta de que **la estructura porcentual de la canasta de consumo (`GRU{i}HD_PCT`) NO discrimina por sí sola la vulnerabilidad financiera familiar**. Un hogar en Déficit Crítico no colapsa por hábitos distorsionados, compras suntuarias o despilfarro en bienes no esenciales (su distribución de compra se solapa de manera homogénea con el estándar nacional). Colapsa porque su **margen monetario Ingreso-Gasto (`BRECHA_PERCAPITA`, `TASA_AHORRO`) es matemáticamente insuficiente** frente al costo absoluto de la canasta de subsistencia. En consecuencia, el Estado no debe intervenir "educando cómo gastar", sino **aliviando la brecha de ingresos mediante transferencias directas y vales alimentarios**.

### 2.5. Nota Técnica sobre Integridad Demográfica y Casos Atípicos (Los 18 Hogares)
Se identificaron exactamente **18 hogares (0.05% de la muestra)** con gasto total anual positivo pero sin desglose registrado en los ocho rubros de consumo (`GRUxxHD = 0`, `GRUxxHD_PCT = 0`).
* **Tratamiento Metodológico:** Se conservan en la tabla de hechos `fact_hogares.csv` (33,691 filas, con la columna `PCA_VALIDO = 0` para estos 18 casos) para no perder cobertura de la muestra. La tabla satélite `fact_hogares_pca.csv`, en cambio, se exporta ya filtrada a **33,673 filas** (excluye a estos 18 hogares sin composición válida), por lo que un `join` en Tableau entre ambas tablas dejará `PC1`/`PC2` nulos para esos 18 registros — comportamiento esperado, no un error de carga.

---

## 3. Diseño Analítico del Dashboard (Historia Visual)

### 3.1. Diseño del Banner Superior y Barra de Filtros (Blindaje Explícito del Alcance)

El banner de la cabecera del **Dashboard Alpha** no utiliza texto genérico, sino una declaración directiva de alcance y filtrado:

* 🏷️ **Título Principal del Tablero:**
  `¿Qué perfiles concentran las mayores brechas entre ingreso y gasto en 2024 y cómo se distribuyen geográficamente?`
* 🏷️ **Subtítulo y Barra de Filtros Explícitos:**
  **`Periodo: 2024 (Enero - Diciembre) | Foco Analítico de KPIs: Hogares en Déficit Crítico (ID_SEGMENTO = 4, 24.5% Ponderado Nacional)`**

> [!IMPORTANT]
> Al declarar en la misma línea de filtros el foco en Déficit Crítico, cualquier persona que abra el dashboard sabe desde el segundo cero que las 4 tarjetas superiores cuantifican exclusivamente el faltante y desahorro de ese estrato vulnerable, mientras que los gráficos inferiores permiten filtrar y comparar los 4 segmentos dinámicamente.

### 3.2. ¿Cómo responde cada Gráfico y KPI a la Pregunta Principal? (Matriz Analítica)

| Elemento del Dashboard | Cláusula de la Pregunta que Responde | Explicación Analítica de la Respuesta |
| :--- | :--- | :--- |
| **Tarjetas Superiores (4 KPIs)** | *"¿Qué perfiles concentran las mayores brechas y de qué magnitud es el problema?"* | Etiquetadas en español claro: 1) `24.5% Hogares en Déficit Crítico` (2.54M familias ponderadas, 23.8% muestral). 2) `-S/ 312 Brecha Monetaria Mensual` (déficit medio por persona en hogares críticos). 3) `-53.7% Tasa Agregada de Desahorro` (promedio ponderado individual: -85.1%). 4) `48.0% Gasto en Alimentos` (rigidez alimentaria inelástica vs. 47.5% en Ahorrador Sólido). |
| **Vista Principal Dominante (Tabla de Texto Resaltada / Highlight Table)** | *"¿Por qué este perfil concentra las mayores brechas entre ingreso y gasto?"* | El Clúster 4 destina el **48.0%** de su gasto a Alimentos (vs. 47.5% del Clúster 1) y **7.1%** a Salud. Mientras el Ahorrador Sólido absorbe ese gasto con holgura líquida (+37.7% ahorro), el Clúster 4 lo enfrenta con una brecha en rojo (-S/ 312 per cápita). |
| **Componente PCA (Scatter Plot: PC1 vs PC2)** | *"¿Se trata de un problema estructural de ingresos o de hábitos de compra superfluos?"* | El solapamiento topológico (silueta casi cero) exime metodológicamente al hogar de culpa: la estructura de compra es homogénea con el resto del país, y el colapso responde a un margen monetario insuficiente. |
| **Soporte A (Barras Horizontales Ordenadas)** | *"¿Cómo se distribuyen estos perfiles según el dominio geográfico y el estrato?"* | Muestra la fractura territorial: Rural de la Sierra Norte, Centro y Selva — Puno (37.3%), Huancavelica (31.2%) y Loreto (30.6%) — frente a Ica (9.0%), con resiliencia. |
| **Soporte B (Línea de Evolución Temporal)** | *"¿Cómo interactúa la brecha con el calendario?"* | Abril registra la mayor incidencia de déficit crítico (27.6%); febrero, la mayor severidad de brecha monetaria media (-S/ 342 per cápita). |
| **Soporte Q&A (Scatter Plot Agregado: Ingreso vs. Gasto)** | *"¿Existe coherencia entre el ingreso neto absoluto y el nivel de gasto operativo en los 4 clústeres?"* | 4 marcas agregadas por `ID_SEGMENTO` en el plano monetario absoluto, separando limpiamente al Clúster 4 del Ahorrador Sólido. |

---

## Referencias Bibliográficas

EconoData Soluciones Perú. (2025). Ensayo: Inflación y coste de vida 2025. Recuperado de https://econodatasolucionesperu.com/wp-content/uploads/2025/04/Ensayo-Inflacion-y-coste-de-vida-2025-N1.pdf

Instituto Nacional de Estadística e Informática (INEI). (2025). Pobreza monetaria afectó al 27,6% de la población del país en el año 2024. Gobierno del Perú. https://www.gob.pe/institucion/inei/noticias/1164173-pobreza-monetaria-afecto-al-27-6-de-la-poblacion-del-pais-en-el-ano-2024

Oxfam en Perú. (2024). ENADES 2024: Encuesta Nacional de Percepción de Desigualdades. https://peru.oxfam.org/ENADES-2024

Instituto Nacional de Estadística e Informática. (s. f.). Microdatos: Sistema de Consulta de Microdatos. Recuperado de https://proyectos.inei.gob.pe/microdatos/
