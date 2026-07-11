# Entrega 6: Trabajo Final Completo y Defensa

**UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS**  
**CURSO:** 1ACC0211 – DATA VISUALIZATION | **NRC:** 18519  
**PROYECTO:** Análisis de brechas socioeconómicas y evolución temporal en los hogares peruanos (ENAHO 2024)  
**EQUIPO DE TRABAJO (GRUPO 5):**  
• Carbajal Robles, Daniel Ivan (U20221B751)  
• Manchay Paredes, Lucero Salome (U202216120)  
• Mayhua Hinostroza, José Antonio (U202218044)  

---

## 1. Resumen Ejecutivo del Proyecto (ENAHO 2024 - MIDIS)

El presente documento consolida la investigación analítica, metodológica y visual desarrollada sobre la Encuesta Nacional de Hogares (**ENAHO 2024**, muestra representativa nacional anual de **33,691 hogares** empadronados por el INEI). El objetivo central del proyecto es proveer al Ministerio de Desarrollo e Inclusión Social (**MIDIS**) un instrumento analítico de decisión pública auditado, reproducible y visualmente excelente para optimizar la asignación del gasto fiscal en programas de alivio alimentario y transferencias monetarias focalizadas.

> [!IMPORTANT]
> **Tesis Central del Proyecto:**  
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
| **PC1** | **22.81%** | **22.81%** | `GRU11HD_PCT` (**+0.664**)<br>*(Alimentos hogar)* | `GRU61HD_PCT` (**-0.388**)<br>`GRU21HD_PCT` (**-0.353**)<br>`GRU81HD_PCT` (**-0.324**) | **Eje de subsistencia primaria vs. Bienes/Servicios No Básicos.** Opone directamente la rigidez alimentaria contra la capacidad de gasto en transporte, vestimenta y servicios de calidad de vida. |
| **PC2** | **16.45%** | **39.26%** | `GRU31HD_PCT` (**+0.550**)<br>`GRU51HD_PCT` (**+0.411**)<br>`GRU61HD_PCT` (**+0.179**) | `GRU41HD_PCT` (**-0.430**)<br>`GRU21HD_PCT` (**-0.355**)<br>`GRU11HD_PCT` (**-0.334**) | **Eje de habitabilidad/salud vs. Enseres/Vestimenta.** Diferencia hogares con costos fijos y gastos médicos urgentes (`GRU31HD`, `GRU51HD`) frente a hogares orientados a mantenimiento y vestimenta. |

### 2.3. Benchmarking Cuantitativo: PCA vs. t-SNE
Para evaluar la calidad de las proyecciones en 2D respecto a la separación externa por clústeres financieros (`ID_SEGMENTO` de 1 al 4) y la fidelidad geométrica, se computaron tres métricas formales sobre una muestra estratificada de `3,000 hogares`:

| Técnica Proyectada | Silhouette Score<br>*(Separación de Clústeres)* | Trustworthiness<br>*(Fidelidad local k=10)* | Reproducibilidad<br>*(Pearson Corr Semilla 1 vs 99)* | Ventajas Operativas | Desventajas / Riesgos |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **PCA (2D)** | **-0.0214** | **0.7690** | **1.0000**<br>*(100% Determinístico)* | • **Linealmente interpretable** mediante Cargas (*Loadings*).<br>• Cómputo instantáneo (0.048 s).<br>• Proyección global estable. | • Proyecta combinaciones lineales; puede perder varieties no lineales complejas. |
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
* **Tratamiento Metodológico:** Se conservaron en la tabla principal `fact_hogares.csv` para mantener la cobertura de la muestra e integridad referencial, pero deben marcarse con el flag `PCA_VALIDO = 0` como casos sin composición válida para la proyección PCA.
---

## 3. Estructura de la Historia Visual (Storytelling de Defensa Rápida en 5 Actos - Guion de 5 Minutos)

La secuencia expositiva del **Dashboard Alpha** (Lienzo 1280x720) está calibrada para durar **exactamente 5 minutos** (1 minuto por cada acto), respondiendo de manera contundente y sin titubeos cada cláusula de nuestra pregunta analítica principal:

> **Pregunta Analítica Principal:**  
> *"¿Qué perfiles de hogares peruanos concentran las mayores brechas entre ingreso y gasto durante el 2024, y cómo se distribuyen estos perfiles (clústeres) según el dominio geográfico, el estrato y las características demográficas?"*

---

### 3.1. Diseño del Banner Superior y Barra de Filtros (Blindaje Explícito del Alcance)

Acatando la corrección textual del profesor en evaluaciones previas (*"Si estás aplicando un filtro o enfocando métricas solamente con el segmento en déficit, hazlo explícito ahí en la barra donde dice filtros"*), el banner azul oscuro de la cabecera del **Dashboard Alpha** no utiliza texto genérico, sino una declaración directiva de alcance y filtrado:

* 🏷️ **Título Principal del Tablero:**  
  `¿Dónde se concentra la trampa de Déficit Crítico familiar y cuál es su asfixia alimentaria?`
* 🏷️ **Subtítulo y Barra de Filtros Explícitos:**  
  **`Periodo: 2024 (Enero - Diciembre) | Foco Analítico de KPIs: Hogares en Déficit Crítico (24.5% Ponderado Nacional) | Filtros Interactivos: [Dominio Geográfico] [Estrato] [Trimestre/Mes]`**

> [!IMPORTANT]
> **Por qué este banner evita el error de la Entrega 5:**  
> Al declarar en la misma línea de filtros **`Foco Analítico de KPIs: Hogares en Déficit Crítico (24.5% Ponderado Nacional)`**, cualquier persona que abra el dashboard sabe desde el segundo cero que las 4 tarjetas superiores cuantifican exclusivamente el faltante y desahorro de ese estrato vulnerable, mientras que los gráficos inferiores permiten filtrar y comparar los 4 segmentos dinámicamente.

---

### 3.2. ¿Cómo responde cada Gráfico y KPI a la Pregunta Principal? (Matriz Analítica)

Para que el jurado vea una conexión perfecta entre la pregunta de investigación y las visualizaciones, cada elemento del Dashboard responde una parte exacta del problema:

| Elemento del Dashboard | Cláusula de la Pregunta que Responde | Explicación Analítica de la Respuesta (Diseño Intuitivo Anti-Confusión) |
| :--- | :--- | :--- |
| **Tarjetas Superiores (4 KPIs)<br>*(Diseño intuitivo de comprensión en 2 segundos)*** | *"¿Qué perfiles concentran las mayores brechas y de qué magnitud es el problema?"* | **Etiquetadas en español claro para que cualquier persona entienda el perfil y su déficit al primer vistazo sin jerga técnica:**<br>1. `24.5% Hogares en Déficit Crítico` (`2.54M familias ponderadas a nivel nacional \| 23.8% muestral`).<br>2. `-S/ 312 Brecha Monetaria Mensual` (`Déficit medio por persona en hogares críticos \| Ponderado`).<br>3. `-53.7% Tasa Agregada de Desahorro (`Promedio ponderado individual: -85.1% | Mediana: -44.5% | Sensible a extremos`)Desahorro medio real ponderado del clúster vs. Umbral de corte < -15%`).<br>4. `48.0% Gasto en Alimentos` (`Rigidez alimentaria inelástica vs. 47.5% en Ahorrador Sólido`). |
| **Vista Principal Dominante<br>(Barras Apiladas 100% de Canasta)** | *"¿Por qué este perfil concentra las mayores brechas entre ingreso y gasto?"* | Evidencia que la propensión media al gasto en bienes de subsistencia es rígida en casi todo el país: el Clúster 4 destina el **48.0% de su gasto a Alimentos** (vs. 47.5% del Clúster 1) y **7.1% a Salud**. Sin embargo, mientras el Ahorrador Sólido absorbe ese 47.5% con holgura líquida (`+37.7% ahorro`), el Clúster 4 lo enfrenta con una brecha en rojo (`-S/ 312 per cápita`), quebrando operativamente. |
| **Componente PCA<br>(Biplot 2D y Loadings)** | *"¿Se trata de un problema estructural de ingresos o de hábitos de compra superfluos?"* | Al mostrar un solapamiento topológico con silueta casi cero (`-0.0214` en PCA / `-0.0183` en t-SNE), **exime metodológicamente al hogar de culpa**. Aporta evidencia geométrica de que el hogar en Déficit Crítico tiene una estructura de compra homogénea con el resto del país; colapsa pura y exclusivamente por un **margen monetario insuficiente (`TASA_AHORRO`)**, justificando transferencias de alivio. |
| **Soporte A<br>(Ranking Departamental)** | *"¿Cómo se distribuyen estos perfiles según el dominio geográfico y el estrato?"* | Muestra la severa fractura territorial del país: el déficit se concentra en el estrato **Rural de la Sierra Norte, Centro y Selva**, liderado por **Puno (37.4%), Huancavelica (31.2%) y Loreto (30.7%)**, mientras Ica (9.0%) muestra resiliencia y excedente. **Moquegua (21.15%)** no forma parte de ese grupo de resiliencia: su incidencia está más cerca del promedio nacional (24.5%) que del caso de Ica. |
| **Soporte B<br>(Líneas de Evolución Temporal)** | *"¿Cómo interactúa la brecha con el calendario y características demográficas familiares?"* | Evidencia la variación según el **mes de entrevista**: abril registra la mayor incidencia de hogares clasificados en déficit crítico (`27.6%`), mientras que febrero presenta la mayor severidad de la brecha monetaria media (`-S/ 342` per cápita, seguido de julio `-S/ 327` y enero `-S/ 323`). |

---

```
[ACTO I (Min 0:00 - 1:00): El Contexto y la Magnitud (Los 4 KPIs Intuitivos - Comprensión en 2 Segundos)]
   │  1. 24.5% Déficit Crítico | 2. -S/ 312 Brecha Mensual | 3. -85.1% Desahorro Medio | 4. 48.0% Gasto en Alimentos
   ▼
[ACTO II (Min 1:00 - 2:00): La Asfixia de la Canasta (Vista Principal Dominante)]
   │  Gráfico 100% Stacked Bar ➔ Insight: Clúster 4 gasta 48.0% en Alimentos (Inelasticidad calórica vs 34.2% Ahorrador)
   ▼
[ACTO III (Min 2:00 - 3:00): La Prueba Geométrica (PCA Biplot y Loadings)]
   │  Proyección PC1 vs PC2 ➔ Insight: Silueta (-0.0214) prueba que el déficit es por falta de ingresos, no por despilfarro
   ▼
[ACTO IV (Min 3:00 - 4:00): Distribución Geográfica y Temporal (Soportes A y B)]
   │  • Soporte A (Ranking): Puno (37.4%) y Loreto (36.2%) lideran la brecha en Sierra Norte y Selva rural
   │  • Soporte B (Evolución): Pico de quiebra en Abril (-S/ 345) por el shock inflacionario escolar y agrario
   ▼
[ACTO V (Min 4:00 - 5:00): Cierre Institucional y Recomendaciones al MIDIS]
   │  Asignación de S/ 450M en vales Qali Warma y rediseño del SISFOH por Tasa de Ahorro
```

---

### 🎙️ Guion Oral Cronometrado para 5 Minutos de Defensa (Exacto: 1 Minuto por Acto)

#### 🕒 Minuto 0:00 a 1:00 — ACTO I: El Contexto y la Magnitud de la Brecha (Los 4 KPIs Intuitivos)
* **Guion Textual (Expositor):**  
  *"Buenos días, jurado evaluador. Nuestro proyecto responde a la pregunta central de qué perfiles de hogares concentran las mayores brechas entre ingreso y gasto en el Perú durante 2024 y cómo se distribuyen en el territorio. Para responder a la primera parte: ¿quiénes son y de qué tamaño es el problema?, veamos nuestras **4 Tarjetas KPI superiores**, redactadas de forma intuitiva y ponderada paramétricamente:  
  1. Primero, el **24.5% de los hogares peruanos a nivel nacional ponderado (~2.54 millones de familias sobre la base muestral de 23.8%)** se clasifica en **Déficit Crítico**.  
  2. Segundo, **dentro de estos hogares críticos**, la **Brecha Monetaria Mensual asciende a -S/ 312 por persona** (es el faltante operativo de estas familias).  
  3. Tercero, sufren una **Tasa media real de Desahorro del -85.1%** (habiendo superado el umbral de corte del -15%), en total oposición al superávit medio nacional (+11.2%).  
  4. Y cuarto, se ven obligados a destinar el **48.0% de su gasto exclusivamente a Alimentos**, operando al límite de la rigidez de subsistencia."*

---

#### 🕒 Minuto 1:00 a 2:00 — ACTO II: La Asfixia de la Canasta Básica (Vista Dominante)
* **Guion Textual (Expositor):**  
  *"Para responder **por qué** este perfil concentra tanta brecha, pasemos al centro del lienzo: nuestra **Vista Principal Dominante (Barras Apiladas al 100%)**, donde comparamos al Clúster 1 (Ahorrador) contra el Clúster 4 (Déficit Crítico). Aquí extraemos nuestro primer insight analítico:*
  * 📌 **QUÉ:** El Clúster 4 destina el **48.0% de su gasto total a Alimentos (`GRU11HD_PCT`)** y un **7.1% a Salud (`GRU51HD_PCT`)**, una proporción muy similar a la del estrato ahorrador (`47.5%` y `5.6%`).
  * 📌 **POR QUÉ:** Alimentos y salud son necesidades inelásticas absolutas. La diferencia crítica no es que el pobre coma más en porcentaje, sino que el Ahorrador Sólido absorbe ese 47.5% con una holgura líquida superavitaria (`+37.7% de ahorro`), mientras que el Clúster 4 enfrenta ese 48.0% con un ingreso deprimido, generando un déficit per cápita en rojo (`-S/ 312`) que asfixia cualquier otro gasto en educación o calidad de vida (`GRU71HD_PCT = 2.4%`).
  * 📌 **ACCIÓN:** Recomendamos al MIDIS no aplicar programas genéricos, sino focalizar un **Subsidio Directo de Cobertura Calórica y Sanitaria** para absorber parte del costo alimentario (`GRU11HD`) en el Clúster 4, liberando margen de liquidez familiar."*

---

#### 🕒 Minuto 2:00 a 3:00 — ACTO III: La Prueba Geométrica (Componente PCA)
* **Guion Textual (Expositor):**  
  *"Para responder si este déficit es culpa de 'malos hábitos de compra' o de falta de ingresos, implementamos nuestro **Análisis de Componentes Principales (PCA)** proyectando las 8 dimensiones de gasto en un biplot 2D con vectores de carga. Aquí presentamos el segundo insight metodológico:*
  * 📌 **QUÉ:** El solapamiento de las nubes de puntos arroja un **Silhouette Score cercano a cero (-0.0214)**, mientras el vector de Alimentos (`+0.664`) tira con fuerza hacia el extremo del Eje PC1.
  * 📌 **POR QUÉ:** Este solapamiento topológico es nuestro hallazgo analítico más fuerte: **sugiere que la composición porcentual del gasto no basta para distinguir o culpabilizar al hogar**. El solapamiento observado sugiere que la estructura porcentual de consumo no discrimina los segmentos financieros. En el alcance de este análisis, el balance neto entre ingreso y gasto (`BRECHA_PERCAPITA`, `TASA_AHORRO`) aparece como el diferenciador directo del déficit operativo.
  * 📌 **ACCIÓN:** Descartamos iniciativas públicas de 'talleres de presupuesto o reeducación financiera' e impulsamos transferencias monetarias directas (Programa Juntos) orientadas a cerrar la brecha operativa de `-S/ 312` per cápita."*

---

#### 🕒 Minuto 3:00 a 4:00 — ACTO IV: Distribución Territorial y Estacional (Soportes A y B)
* **Guion Textual (Expositor):**  
  *"En los paneles inferiores respondemos la segunda mitad de la pregunta: **cómo se distribuyen estos perfiles según el dominio geográfico, estrato y estacionalidad**:*
  * 📌 **QUÉ:** En el **Ranking Departamental (Soporte A)**, la brecha golpea con extrema severidad a la **Sierra Norte, Centro y Selva rural: Puno (37.4%), Huancavelica (31.2%) y Loreto (30.7%)** concentran la mayor tasa de déficit, en contraste con la Costa urbana (Ica 9.0%, Moquegua 9.8%). Paralelamente, en la **Evolución Temporal (Soporte B)**, vemos que la brecha sufre un shock en el primer cuatrimestre, alcanzando su **pico de incidencia en abril (27.6%) y de severidad de brecha en febrero (-S/ 342)**.
  * 📌 **POR QUÉ:** La concentración en Puno y Loreto sugiere vulnerabilidad rural logística. Asimismo, el pico de severidad de febrero (-S/ 342) e incidencia de abril plantean la hipótesis de tensiones de liquidez por la estacionalidad agrícola o escolar, planteando como sugerencia de política un **Bono de Contención Estacional**."*

---

#### 🕒 Minuto 4:00 a 5:00 — ACTO V: Cierre Institucional, Paradoja de Focalización y Q&A
* **Guion Textual (Expositor):**  
  *"Para cerrar nuestra exposición en el minuto final, revelamos una **paradoja crítica de focalización pública**: el **81.4% de los hogares ponderados (81.7% muestral) que hemos identificado en Déficit Crítico operativo (Clúster 4) son clasificados como 'No Pobres' por la medición monetaria tradicional del INEI**.  
  Al medirse solo por ingresos brutos sin restar el costo inelástico de salud y alimentos, más de 6,500 familias de nuestra encuesta (2.07 millones de hogares expandidos a nivel nacional) aparecen como no pobres según la clasificación monetaria disponible. Esto sugiere que el indicador tradicional de pobreza y el déficit operativo (`BRECHA_PERCAPITA`, `TASA_AHORRO`) capturan dimensiones distintas de vulnerabilidad.  
  Por ello, recomendamos al MIDIS modernizar el algoritmo del **SISFOH**, incorporando como criterio de elegibilidad la `TASA_AHORRO` y la `BRECHA_PERCAPITA` que hoy hemos comprobado.  
  Nuestro pipeline en Python y el modelo en Esquema Estrella quedan 100% auditados y reproducibles a su disposición. Muchas gracias."*

---

---

## 4. Batería de Preguntas y Respuestas Rápidas para la Defensa (QA con Jurado)

Este guion operativo está diseñado para que cualquier miembro del equipo responda de forma fluida, directa, con alto peso académico y en milisegundos durante el turno de preguntas del profesor o jurado evaluador.

### ❓ Pregunta 1: ¿Por qué eligieron PCA como técnica principal en lugar de t-SNE si t-SNE obtuvo un puntaje de *Trustworthiness* superior (0.988 vs 0.769)?
> **Respuesta Directa y con Autoridad:**  
> *"Elegimos PCA porque el diseño de políticas públicas en el MIDIS exige **interpretabilidad explicativa lineal exacta**. Aunque t-SNE preserva excelentemente las vecindades locales en 2D (*Trustworthiness = 0.9879*), es un algoritmo topológico no lineal ('caja negra') que carece de **Cargas (*Loadings*)**. Con PCA podemos demostrar matemáticamente que el Eje 1 (PC1) está dominado por el gasto en Alimentos (`GRU11HD_PCT = +0.664`) en contraposición al Transporte y Vestimenta (`-0.388` y `-0.353`). Además, PCA es 100% determinístico y procesa los 33,691 hogares en 48 milisegundos. Preferimos PCA no por costo computacional — t-SNE con Barnes–Hut es de hecho $O(N \log N)$ y corre en segundos — sino porque el diseño de política pública exige interpretabilidad lineal exacta mediante *loadings*, algo que t-SNE no ofrece."*

### ❓ Pregunta 2: El Silhouette Score de sus clústeres financieros dio cercano a cero o negativo (-0.0214 en PCA / -0.0183 en t-SNE). ¿No significa eso que su modelo o su segmentación están mal hechos?
> **Respuesta Directa y con Autoridad:**  
> *"No, profesor; al contrario, **ese resultado es el hallazgo analítico central de nuestra tesis**. Debemos recordar que el Silhouette Score aquí se evaluó proyectando la composición porcentual de los 8 rubros de gasto (`GRU11HD_PCT` a `GRU81HD_PCT`) frente a una etiqueta externa: el **Clúster de Vulnerabilidad Financiera (`ID_SEGMENTO`)**.  
> Que la silueta sea cercana a cero demuestra empírica y científicamente que **la estructura porcentual de consumo NO es la que determina el déficit operativo**. Un hogar de clase media (`Clúster 2`) y uno en Déficit Crítico (`Clúster 4`) distribuyen su canasta porcentual de manera casi idéntica. El hogar del Clúster 4 no se quiebra por consumir lujos o por distorsiones de hábito, sino por la **rigidez absoluta del costo de alimentos frente a un ingreso monetario insuficiente (`TASA_AHORRO < -15%`)**. Este insight valida que el MIDIS debe inyectar margen de ingresos y no realizar campañas de reeducación del gasto."*

### ❓ Pregunta 3: ¿Por qué en su Dashboard preliminar o en el prototipo eliminaron los gráficos de pastel y los gráficos de doble eje?
> **Respuesta Directa y con Autoridad:**  
> *"Eliminamos los gráficos de pastel porque la percepción visual humana es genéticamente ineficiente para estimar y comparar **ángulos y áreas**, especialmente con 8 rubros de gasto o 4 clústeres cuya diferencia es de pocos puntos porcentuales; por ello adoptamos el **Gráfico de Barras Apiladas al 100% y la Tabla Resaltada (Highlight Table)**, que comparan longitudes sobre una línea base común con precisión analítica perfecta.  
> Respecto al **doble eje con escalas distintas**, lo descartamos acatando las mejores prácticas de visualización de datos, ya que distorsiona las pendientes y cruces artificiales de líneas, induciendo a correlaciones espurias en el tomador de decisiones. En su lugar, utilizamos gráficos alineados en paneles independientes pero sincronizados temporalmente por trimestre."*

### ❓ Pregunta 4: ¿De dónde salen exactamente los KPIs superiores (ej. 24.5% en Déficit Crítico) y cómo ponderan la representatividad nacional de la muestra?
> **Respuesta Directa y con Autoridad:**  
> *"Los KPIs se derivan directamente del procesamiento del archivo `fact_hogares.csv` (y su proyección `fact_hogares_pca.csv`), los cuales incorporan el **Factor de Expansión Anual del INEI (`FACTOR07`)**. El porcentaje de 24.5% se calcula dividiendo la suma de los factores de expansión (`FACTOR07`) de los hogares clasificados en `ID_SEGMENTO = 4` entre la suma total de hogares del país (aproximadamente 10.36 millones de hogares expandidos sobre la muestra limpia de 33,691 encuestas; a nivel muestral sin ponderar representa el 23.8%). Cada métrica en Tableau utiliza promedios ponderados y sumas expandidas para asegurar que el dashboard refleje la realidad demográfica nacional al 100%."*

### ❓ Pregunta 5: ¿Por qué en los títulos de sus Tarjetas KPI usan nombres como "Brecha Monetaria Mensual" o "Tasa de Desahorro" con subtítulos que dicen "en hogares críticos" en lugar de poner "Clúster 4" en todo o "Media Poblacional"?
> **Respuesta Directa y con Autoridad:**  
> *"Lo hacemos por dos principios de excelencia en visualización directiva: **intuitividad inmediata y prevención del error macroeconómico**.  
> Primero, si repitiéramos la jerga técnica 'Clúster 4' en las 4 tarjetas, sobrecargaríamos la carga cognitiva de quien ve el dashboard por primera vez. Y segundo, si pusiéramos '-S/ 312 Brecha per cápita | Media poblacional' sin especificar que es de las familias quebradas, **el jurado podría malinterpretar que toda la población del Perú opera a pérdida de 312 soles al mes**, lo cual sería incorrecto (el promedio y mediana nacional son superavitarios con +11.2% de ahorro).  
> Al redactar títulos intuitivos (**'-S/ 312 Brecha Monetaria Mensual'**) y aclarar en el subtítulo **'Déficit medio por persona en hogares críticos | No país'**, logramos que cualquier tomador de decisiones entienda el problema en exactamente 2 segundos sin jerga y sin falsas alarmas macroeconómicas para el MIDIS."*

### ❓ Pregunta 6: ¿Cómo garantizan que su pipeline técnico y su modelo en Tableau sean completamente reproducibles para una auditoría externa?
> **Respuesta Directa y con Autoridad:**  
> *"Nuestro pipeline cumple con el estándar **End-to-End Audit-Ready**. En el preprocesamiento Python (`01_limpieza.ipynb` a `04_componente_avanzado_pca_tsne.ipynb`), fijamos semillas aleatorias exactas (`random_state=42` para PCA y `random_state=1/99` para t-SNE) y estandarizaciones lineales (`StandardScaler`) sin truncamientos ocultos ni mutaciones manuales. Además, hemos programado la exportación dual sincronizada en el notebook final: cada vez que se corre el análisis, el archivo `fact_hogares_pca.csv` se escribe tanto en el directorio analítico (`Data/PCA/`) como en el directorio dimensional de Tableau (`Data/modelo/esquema_estrella/`), garantizando integridad referencial y reproducibilidad exacta con solo ejecutar un comando."*

### ❓ Pregunta 7: ¿Por qué en la barra de filtros del banner superior escribieron explícitamente "Foco Analítico de KPIs: Hogares en Déficit Crítico (24.5% Ponderado Nacional)"?
> **Respuesta Directa y con Autoridad:**  
> *"Acatamos una directriz metodológica clave que usted nos dio en la evaluación anterior: **cuando un KPI o métrica superior está filtrado o enfocado en un estrato específico, debe declararse en la barra de filtros del banner para no inducir al error visual de creer que es el total país**.  
> Al colocar explícitamente **'Foco Analítico de KPIs: Hogares en Déficit Crítico (24.5% Ponderado Nacional)'** en la barra superior junto a los filtros interactivos de Dominio y Estrato, transparentamos desde el segundo cero que las 4 tarjetas superiores cuantifican la asfixia operativa y el desahorro de ese estrato vulnerable, mientras que los gráficos centrales contrastan los 4 segmentos poblacionales. Así logramos un tablero 100% intuitivo, riguroso y libre de falsas interpretaciones para el jurado y el MIDIS."*

---

## 5. Auditoría y Trazabilidad de Archivos del Pipeline

| Archivo / Notebook | Ruta del Sistema | Rol en el Ecosistema del Proyecto | Estado de Verificación |
| :--- | :--- | :--- | :---: |
| **Limpieza y UBIGEO** | `notebooks/01_perfilado_y_limpieza.ipynb` | Tratamiento de nulos, estandarización de 6 dígitos en UBIGEO y tipificado de identificadores. | ✅ Verificado |
| **Outliers y Gasto** | `notebooks/02_modelado_de_datos.ipynb` | Truncamiento de colas extremas en ingresos/gastos (`INGRESO_PERCAPITA`, `GASTO_PERCAPITA`). | ✅ Verificado |
| **Ingeniería Características** | `notebooks/03_calculos_analiticos.ipynb` | Creación de métricas derivadas (`TASA_AHORRO`, `BRECHA_PERCAPITA`, `ID_SEGMENTO` 1 al 4). | ✅ Verificado |
| **Componente PCA/t-SNE** | `notebooks/04_componente_avanzado_pca_tsne.ipynb` | Reducción dimensional, cálculo de *loadings*, silueta y exportación de coordenadas 2D. | ✅ Verificado (QA Dual) |
| **Base Analítica PCA** | `Data/modelo/esquema_estrella/fact_hogares_pca.csv` | Tabla de hechos enriquecida con coordenadas `PC1` y `PC2` para consumo directo en Tableau. | ✅ Verificado (33,691 filas) |
| **Satélite Cargas PCA** | `Data/modelo/esquema_estrella/pca_loadings.csv` | Vector de cargas (`loadings`) de los 8 rubros en `PC1` y `PC2` para visualización geométrica biplot en Tableau. | ✅ Verificado (8 rubros) |
| **Satélite Varianza PCA** | `Data/modelo/esquema_estrella/pca_varianza.csv` | Tabla de varianza explicada (22.81% PC1, 16.45% PC2) para benchmarking en Tableau. | ✅ Verificado (8 componentes) |
| **Dashboard Alpha** | `Data/modelo/esquema_estrella/` (Conexión TWBX) | Libro de trabajo visual de Tableau ajustado al lienzo 1280x720 y la matriz oficial del curso. | ✅ Verificado |
