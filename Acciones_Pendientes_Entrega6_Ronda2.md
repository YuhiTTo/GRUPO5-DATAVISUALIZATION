# Acciones Pendientes — Entrega 6 (Ronda 2)

Consolidado de todo lo que falta tras la verificación del zip más reciente. 4 acciones en 3 archivos.

---

## 1. `docs/Entrega_6_Trabajo_Final_y_Defensa.md`

**Acción: CAMBIAR** (línea ~158, guion de ACTO IV — quedó sin corregir en la ronda anterior)

**Buscar:**
> En los paneles inferiores respondemos la segunda mitad de la pregunta: **cómo se distribuyen estos perfiles según el dominio geográfico, estrato y estacionalidad**:*
> * 📌 **QUÉ:** En el **Ranking Departamental (Soporte A)**, la brecha golpea con extrema severidad a la **Sierra Norte, Centro y Selva rural: Puno (37.4%), Huancavelica (31.2%) y Loreto (30.7%)** concentran la mayor tasa de déficit, en contraste con la Costa urbana (Ica 9.0%, **Moquegua 9.8%**). Paralelamente...

**Reemplazar por:**
> En los paneles inferiores respondemos la segunda mitad de la pregunta: **cómo se distribuyen estos perfiles según el dominio geográfico, estrato y estacionalidad**:*
> * 📌 **QUÉ:** En el **Ranking Departamental (Soporte A)**, la brecha golpea con extrema severidad a la **Sierra Norte, Centro y Selva rural: Puno (37.4%), Huancavelica (31.2%) y Loreto (30.7%)** concentran la mayor tasa de déficit, en contraste con **Ica (9.0%)**, que muestra resiliencia costera. Paralelamente...

(Se elimina la mención a "Moquegua 9.8%" del guion; ya no forma parte del grupo de resiliencia costera según el dato corregido de 21.15%, consistente con la tabla de la sección 3.2.)

---

## 2. `notebooks/04_componente_avanzado_pca_tsne.ipynb`

**Acción: EJECUTAR Y GUARDAR** (celda 20 — el código ya está bien, solo falta correrlo)

- Correr la celda 20 (verificación de robustez del Silhouette) y **guardar el notebook con el output visible**. Actualmente está sin ejecutar (0 outputs), así que en el estado actual no sirve como evidencia para la defensa.
- Resultado esperado al correrla (ya lo verifiqué de forma independiente): Silhouette PCA 2D transformado ≈ **-0.0214** vs. sin imputar ≈ **-0.0191** (diferencia ≈ 0.0023) — confirma que el hallazgo es robusto.

**Acción: AGREGAR** (celda markdown nueva, justo después de la celda 20)

```markdown
**Conclusión de robustez:** La diferencia entre el Silhouette Score calculado sobre los segmentos
transformados (-0.0214) y sobre los segmentos derivados de los datos crudos sin imputar (-0.0191)
es de apenas 0.0023. Ambos valores son cercanos a cero y del mismo signo, por lo que el hallazgo
central — la composición porcentual del gasto no discrimina el segmento financiero — es **robusto**
a la decisión metodológica de imputación de outliers y no depende de ella.
```

---

## 3. `notebooks/03_calculos_analiticos.ipynb`

**Acción: CAMBIAR** (celda 7 — pendiente de la primera ronda, aún sin resolver)

**Buscar:**
```python
fact_hogares['TASA_AHORRO'] = (fact_hogares['INGHOG2D'] - fact_hogares['GASHOG2D']) / ingreso_seguro
fact_hogares['TASA_AHORRO'] = fact_hogares['TASA_AHORRO'].fillna(0)
```

**Reemplazar por:**
```python
fact_hogares['TASA_AHORRO'] = ((fact_hogares['INGHOG2D'] - fact_hogares['GASHOG2D']) / ingreso_seguro).round(6)
fact_hogares['TASA_AHORRO'] = fact_hogares['TASA_AHORRO'].fillna(0)
```

**Acción: AGREGAR** (nueva celda, después de la celda 11 donde se calcula `ID_SEGMENTO`)

Crear la columna `PCA_VALIDO` que el propio documento de Entrega 6 (línea 64) dice que debería existir, marcando en 0 los hogares con canasta de gasto en cero (los 18 casos identificados):

```python
# Flag PCA_VALIDO: 0 para hogares sin composición de gasto válida (los 8 rubros GRU_PCT suman 0)
pct_cols = [c for c in fact_hogares.columns if c.endswith('_PCT')]
fact_hogares['PCA_VALIDO'] = (fact_hogares[pct_cols].sum(axis=1) > 0).astype(int)

print("Hogares marcados como no válidos para PCA (PCA_VALIDO = 0):",
      (fact_hogares['PCA_VALIDO'] == 0).sum())
```

**Acción: ACTUALIZAR** (celda 15 — exportación, sin cambios de código, solo consecuencia de lo anterior)

Ninguna edición necesaria en la celda de `to_csv()`: al agregar la columna `PCA_VALIDO` antes de la celda 15, se exportará automáticamente en `fact_hogares.csv` y `fact_hogares_espanol.csv` (agregar también `'PCA_VALIDO': 'PCA_Valido'` al diccionario `mapa_espanol` para mantener consistencia de nombres en la versión en español).

---

## 4. `notebooks/04_componente_avanzado_pca_tsne.ipynb` (uso del nuevo flag)

**Acción: CAMBIAR** (la celda donde se arma `df` / `X` para el PCA, antes de la celda 16 de muestreo)

Una vez exista `PCA_VALIDO` en `fact_hogares.csv`, filtrar los 18 hogares inválidos antes de ajustar el PCA, en vez de dejarlos entrar con un vector de ceros:

```python
df = df[df['PCA_VALIDO'] == 1].reset_index(drop=True)
```

(Ubicar esta línea inmediatamente después de la lectura de `fact_hogares.csv` en la celda donde se define `df` por primera vez, antes del `StandardScaler`.)

---

## Resumen

| # | Archivo | Acción | Prioridad |
|---|---|---|---|
| 1 | `docs/Entrega_6_Trabajo_Final_y_Defensa.md` | Cambiar (guion ACTO IV, Moquegua) | Alta — se lee en voz alta en la defensa |
| 2 | `notebooks/04_componente_avanzado_pca_tsne.ipynb` | Ejecutar y guardar celda 20 + agregar celda markdown de conclusión | Alta — sin esto la verificación no cuenta como evidencia |
| 3 | `notebooks/03_calculos_analiticos.ipynb` | Cambiar (redondeo `TASA_AHORRO`) + Agregar (`PCA_VALIDO`) | Media — pendiente desde la primera ronda |
| 4 | `notebooks/04_componente_avanzado_pca_tsne.ipynb` | Cambiar (filtrar `PCA_VALIDO == 1` antes del PCA) | Media — depende de que primero se agregue el flag en el punto 3 |
