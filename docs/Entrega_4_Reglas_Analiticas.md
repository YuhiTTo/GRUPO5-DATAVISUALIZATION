# Entrega 4: Reglas Analíticas y Segmentación

Este documento detalla la estructura lógica, las métricas derivadas y la segmentación implementadas para construir el **Esquema Estrella Analítico** que consumirá Tableau.

## 1. Validación de la Estructura Relacional
Se mantiene la arquitectura centralizada (`fact_hogares` conectada a múltiples dimensiones). 
Para cumplir estrictamente con los criterios de Tableau y evitar duplicidad de métricas, se generó una nueva dimensión analítica (`dim_segmento`) en lugar de sobrecargar la tabla de hechos con cadenas de texto. 

> [!IMPORTANT]
> **Validación Técnica para Tableau:**
> Todas las llaves foráneas en `fact_hogares`, incluyendo la nueva llave `ID_SEGMENTO`, han sido validadas mediante scripts de Python para garantizar **ausencia absoluta de valores Nulos (NaN)** y han sido forzadas al tipo de dato **Entero (Integer)**. Esto asegura una conexión nativa y fluida en Tableau sin requerir reprocesamiento manual ni limpieza adicional por parte del usuario final.

## 2. Métricas Derivadas
Se generó una métrica clave para responder a la pregunta analítica del proyecto referente a las brechas socioeconómicas:

*   **`TASA_AHORRO` (Margen de Brecha Relativa):**
    *   **Fórmula:** `(INGHOG2D - GASHOG2D) / INGHOG2D`
    *   **Interpretación:** Mide qué porcentaje de su ingreso total logra ahorrar el hogar, o en su defecto, qué porcentaje de déficit asume. Una tasa de `0.15` indica que el hogar ahorra el 15% de su sueldo. Una tasa de `-0.20` indica que gasta un 20% más de lo que ingresa. Esto permite comparar el impacto de una brecha de "500 soles" entre un hogar de bajos recursos frente a uno de altos recursos.
    *   **Nota Visual (Outliers):** Existen algunos hogares excepcionales (con ingresos ínfimos pero alto gasto) cuyas tasas pueden ser muy negativas (ej. `-10` o `-171`). Son analíticamente válidos y no deben eliminarse del dataset, pero para la visualización en Tableau (ej. en histogramas), se recomienda aplicar un filtro visual en el eje limitando el rango a `[-2, 1]` para evitar el colapso de la escala general.

## 3. Segmentación: Perfiles de Ahorro y Déficit (Clústeres Analíticos)
Con base en la `TASA_AHORRO`, se agrupó a los hogares en 4 perfiles (clústeres) que permiten analizar dónde se concentran los mayores riesgos financieros, independientemente de la clasificación de pobreza del INEI:

1.  **Ahorrador Sólido (`ID_SEGMENTO = 1`):** `TASA_AHORRO >= 15%`. Hogares con alta holgura económica mensual. (COLOR_HEX: `#2CA02C`)
2.  **Equilibrio / Supervivencia (`ID_SEGMENTO = 2`):** `0% <= TASA_AHORRO < 15%`. Hogares que cubren sus gastos pero con nula o escasa capacidad de ahorro. Vulnerables ante shocks. (COLOR_HEX: `#FF7F0E`)
3.  **Déficit Leve (`ID_SEGMENTO = 3`):** `-15% <= TASA_AHORRO < 0%`. Hogares que gastan hasta un 15% por encima de sus ingresos, posiblemente apalancados en deuda a corto plazo. (COLOR_HEX: `#D62728`)
4.  **Déficit Crítico (`ID_SEGMENTO = 4`):** `TASA_AHORRO < -15%`. Hogares en estrés financiero severo. (COLOR_HEX: `#8C564B`)

## 4. Lógica de Parámetros Recomendada (Para aplicar en Tableau)
Se sugiere crear un **Parámetro Dinámico ("Simulador de Shocks Económicos")** en Tableau con la siguiente lógica:
*   **Crear Parámetro:** `[Inflación Alimentos]` (Rango: 0 a 0.50).
*   **Crear Campo Calculado:** `Gasto_Simulado = GASHOG2D + (GRU11HD * [Inflación Alimentos])`.
*   **Explicación:** Permite al usuario interactuar con el Dashboard, incrementando virtualmente el costo de los alimentos para observar en tiempo real cuántos hogares caerían del clúster "Equilibrio" al clúster "Déficit Crítico".

## 5. Nota Analítica: Limitación Temporal (Corte Transversal)
> [!NOTE]
> **Limitación Metodológica:**
> El dataset ENAHO 2024 utilizado en este proyecto es un estudio de **corte transversal**, no longitudinal. Esto significa que la dimensión de tiempo (`dim_tiempo`) no traza la evolución de un mismo hogar a lo largo de los meses, sino que agrupa a distintos hogares encuestados en un mes determinado. Cualquier visualización temporal en Tableau reflejará tendencias estacionales agregadas de la muestra, pero no la historia financiera individual de una familia.
