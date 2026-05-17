import pandas as pd
import numpy as np
import os

print("--- 1. Cargando dataset limpio ---")
df = pd.read_csv('Data/limpio/Sumaria-2024_limpio.csv')

# Arreglando pérdida de ceros a la izquierda en UBIGEO (Pandas lo lee como int por defecto)
df['UBIGEO'] = df['UBIGEO'].astype(str).str.zfill(6)

df.insert(0, 'ID_HOGAR', range(1, len(df) + 1))

os.makedirs('Data/modelo', exist_ok=True)
os.makedirs('Data/modelo/tabla_plana', exist_ok=True)
os.makedirs('Data/modelo/esquema_estrella', exist_ok=True)
os.makedirs('Data/modelo/copo_de_nieve', exist_ok=True)

print("--- 2. Exportando Tabla Plana (Flat Table) ---")
df.to_csv('Data/modelo/tabla_plana/Sumaria-2024_flat.csv', index=False, encoding='utf-8-sig')

print("--- 3. Generando Esquema Estrella (Star Schema) ---")
dim_geografia = df[['UBIGEO', 'DEPARTAMENTO', 'DOMINIO', 'ESTRATO']].drop_duplicates().reset_index(drop=True)
dim_geografia.insert(0, 'ID_GEOGRAFIA', range(1, len(dim_geografia) + 1))

dim_tiempo = df[['MES_NUM', 'MES']].drop_duplicates().sort_values('MES_NUM').reset_index(drop=True)

dim_pobreza = df[['POBREZA', 'POBREZAV', 'EN_DEFICIT']].drop_duplicates().reset_index(drop=True)
dim_pobreza.insert(0, 'ID_POBREZA', range(1, len(dim_pobreza) + 1))

# Tabla de hechos
df_facts = df.merge(dim_geografia, on=['UBIGEO', 'DEPARTAMENTO', 'DOMINIO', 'ESTRATO'], how='left')
df_facts = df_facts.merge(dim_pobreza, on=['POBREZA', 'POBREZAV', 'EN_DEFICIT'], how='left')

claves = ['ID_HOGAR', 'ID_GEOGRAFIA', 'MES_NUM', 'ID_POBREZA']
metricas = [
    'MIEPERHO', 'FACTOR07', 'INGHOG2D', 'GASHOG2D', 'BRECHA_HOG',
    'ING_PERCAPITA', 'GAS_PERCAPITA', 'BRECHA_PERCAPITA',
    'LOG_INGHOG2D', 'LOG_GASHOG2D', 'LOG_BRECHA_PERCAP'
]
columnas_grupos = [col for col in df.columns if col.startswith('GRU')]
fact_hogares = df_facts[claves + metricas + columnas_grupos]

# Exportar Estrella
dim_geografia.to_csv('Data/modelo/esquema_estrella/dim_geografia.csv', index=False, encoding='utf-8-sig')
dim_tiempo.to_csv('Data/modelo/esquema_estrella/dim_tiempo.csv', index=False, encoding='utf-8-sig')
dim_pobreza.to_csv('Data/modelo/esquema_estrella/dim_pobreza.csv', index=False, encoding='utf-8-sig')
fact_hogares.to_csv('Data/modelo/esquema_estrella/fact_hogares.csv', index=False, encoding='utf-8-sig')

print("--- 4. Generando Esquema Copo de Nieve (Snowflake Schema) ---")
# Rompemos dim_geografia en dos
dim_departamento = dim_geografia[['DEPARTAMENTO']].drop_duplicates().reset_index(drop=True)
dim_departamento.insert(0, 'ID_DEP', range(1, len(dim_departamento) + 1))

dim_geografia_snow = dim_geografia.merge(dim_departamento, on='DEPARTAMENTO', how='left')
dim_geografia_snow = dim_geografia_snow[['ID_GEOGRAFIA', 'UBIGEO', 'ID_DEP', 'DOMINIO', 'ESTRATO']]

# Exportar Snowflake
dim_departamento.to_csv('Data/modelo/copo_de_nieve/dim_departamento.csv', index=False, encoding='utf-8-sig')
dim_geografia_snow.to_csv('Data/modelo/copo_de_nieve/dim_geografia_snow.csv', index=False, encoding='utf-8-sig')
dim_tiempo.to_csv('Data/modelo/copo_de_nieve/dim_tiempo.csv', index=False, encoding='utf-8-sig')
dim_pobreza.to_csv('Data/modelo/copo_de_nieve/dim_pobreza.csv', index=False, encoding='utf-8-sig')
fact_hogares.to_csv('Data/modelo/copo_de_nieve/fact_hogares.csv', index=False, encoding='utf-8-sig')


print("--- 5. Ejecutando Benchmarking (Memoria RAM) ---")
def calcular_memoria(dfs):
    total_bytes = sum(d.memory_usage(deep=True).sum() for d in dfs)
    return total_bytes / (1024 * 1024) # A Megabytes

mem_flat = calcular_memoria([df])
mem_star = calcular_memoria([fact_hogares, dim_geografia, dim_tiempo, dim_pobreza])
mem_snow = calcular_memoria([fact_hogares, dim_geografia_snow, dim_departamento, dim_tiempo, dim_pobreza])

resultados = pd.DataFrame({
    'Modelo': ['Tabla Plana (Base)', 'Esquema Estrella (Opcion 1)', 'Copo de Nieve (Opcion 2)'],
    'Memoria RAM (MB)': [mem_flat, mem_star, mem_snow],
    'Reduccion vs Base (%)': [0, (1 - mem_star/mem_flat)*100, (1 - mem_snow/mem_flat)*100],
    'Saltos de Join Topologicos': [0, 1, 2]
})

print("--- 6. Simulación de Escalabilidad Histórica (Proyección a 5 años) ---")
# Multiplicamos la data transaccional simulando la inyección de 5 encuestas anuales
df_5y = pd.concat([df]*5, ignore_index=True)
fact_hogares_5y = pd.concat([fact_hogares]*5, ignore_index=True)

# Las dimensiones no se multiplican porque los departamentos y estratos no cambian (permanecen estáticos)
mem_flat_5y = calcular_memoria([df_5y])
mem_star_5y = calcular_memoria([fact_hogares_5y, dim_geografia, dim_tiempo, dim_pobreza])
mem_snow_5y = calcular_memoria([fact_hogares_5y, dim_geografia_snow, dim_departamento, dim_tiempo, dim_pobreza])

resultados['Memoria Proyectada 5 Años (MB)'] = [mem_flat_5y, mem_star_5y, mem_snow_5y]

print(resultados.round(2))
resultados.to_csv('Data/modelo/benchmarking_resultados.csv', index=False, encoding='utf-8-sig')
print("¡Benchmarking completado y resultados exportados!")
