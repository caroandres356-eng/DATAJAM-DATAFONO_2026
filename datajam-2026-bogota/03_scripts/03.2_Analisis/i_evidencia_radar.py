import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import unicodedata
import numpy as np
import os

os.makedirs('../02_graficas', exist_ok=True)

def norm(s):
    s = str(s).strip()
    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').upper()

print("Cargando datos para evidencia del radar...")
df_id = pd.read_excel('../01_datos/processed/p_salud_ideacion.xlsx')
df_sui = pd.read_excel('../01_datos/processed/p_salud_suicidio.xlsx')
df_dep = pd.read_excel('../01_datos/processed/p_programas_deporte.xlsx', header=2)

# Limpiar y normalizar localidades
df_id['loc'] = df_id['localidad_residencia'].apply(norm)
df_sui['loc'] = df_sui['LOCALIDAD_DEL_HECHO'].apply(norm)
df_dep.columns = [str(c).strip() for c in df_dep.columns]
df_dep = df_dep[df_dep['Localidad'].notna()]
df_dep['loc'] = df_dep['Localidad'].apply(norm)
df_dep['Total'] = pd.to_numeric(df_dep['Total'], errors='coerce')

excluir = ['SIN DATO','','BOGOTA','LOCALIDAD DESCONOCIDA', 'SUMAPAZ']

# Agrupar
ideacion = df_id.groupby('loc').size().reset_index(name='ideacion')
suicidios = df_sui[~df_sui['loc'].isin(excluir)].groupby('loc').size().reset_index(name='suicidios')
deporte = df_dep.groupby('loc')['Total'].sum().reset_index(name='participantes')

# Hacer merge de las tres variables clave
df = ideacion.merge(suicidios, on='loc').merge(deporte, on='loc')
df = df[~df['loc'].isin(excluir)]

# Calcular la letalidad (Tasa de conversión)
df['tasa_conversion'] = (df['suicidios'] / df['ideacion']) * 100

print("Generando gráfica i1...")
fig, ax = plt.subplots(figsize=(11,7))

# Scatter plot: x = participantes en deporte, y = tasa de letalidad
sc = ax.scatter(df['participantes'], df['tasa_conversion'], 
                s=df['ideacion']/40, color='#E24B4A', alpha=0.8, edgecolors='#333', zorder=3)

# Etiquetas de las localidades
for _, row in df.iterrows():
    ax.annotate(row['loc'], (row['participantes'], row['tasa_conversion']), 
                fontsize=8, ha='left', va='bottom', color='#222')

# Línea de tendencia (Regresión lineal)
coef = np.polyfit(df['participantes'], df['tasa_conversion'], 1)
xline = np.linspace(df['participantes'].min(), df['participantes'].max(), 100)
ax.plot(xline, coef[0]*xline+coef[1], '--', color='gray', linewidth=1.5, 
        label=f'Tendencia (Más deporte = Menor letalidad)', zorder=2)

ax.set_xlabel('Participantes en Programas Institucionales (El Radar Deportivo)', fontsize=11)
ax.set_ylabel('Tasa de Letalidad (% de casos de ideación que terminan en suicidio)', fontsize=11)
ax.set_title('Evidencia del "Radar Institucional": \nA mayor cobertura de programas, menor es la letalidad por detección temprana\n(Tamaño de la burbuja = Casos totales de ideación)', fontsize=13)

ax.legend()
plt.tight_layout()
plt.savefig('../02_graficas/i1_evidencia_radar.png', dpi=150)
plt.close()

print("¡Listo! Gráfica generada en 02_graficas/i1_evidencia_radar.png")