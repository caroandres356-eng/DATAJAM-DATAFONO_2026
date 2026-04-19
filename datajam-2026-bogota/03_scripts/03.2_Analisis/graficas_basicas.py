import pandas as pd 
import matplotlib 
matplotlib.use('Agg') 
import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
import unicodedata, os 
 
def norm(s): 
    s = str(s).strip() 
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper() 
 
os.makedirs('../02_graficas', exist_ok=True) 
 
# --- IDEACION --- 
df_id = pd.read_excel('../01_datos/processed/p_salud_ideacion.xlsx') 
df_id['loc'] = df_id['localidad_residencia'].apply(norm) 
 
# grafica 1: ranking por localidad 
casos_loc = df_id.groupby('loc').size().reset_index(name='casos').sort_values('casos', ascending=True) 
fig, ax = plt.subplots(figsize=(10,7)) 
ax.barh(casos_loc['loc'], casos_loc['casos'], color='#378ADD') 
ax.set_xlabel('Casos de ideacion/intento suicida') 
ax.set_title('Casos por localidad (2019-2023)') 
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}')) 
plt.tight_layout() 
plt.savefig('../02_graficas/g1_ideacion_por_localidad.png', dpi=150) 
plt.close() 
print('g1 ok') 
 
# grafica 2: tendencia anual 
tendencia = df_id.groupby('ano_notificacion').size().reset_index(name='casos') 
fig, ax = plt.subplots(figsize=(9,5)) 
ax.plot(tendencia['ano_notificacion'], tendencia['casos'], marker='o', color='#378ADD', linewidth=2) 
ax.fill_between(tendencia['ano_notificacion'], tendencia['casos'], alpha=0.15, color='#378ADD') 
ax.set_title('Tendencia anual de ideacion suicida en Bogota') 
ax.set_xlabel('Ano') 
ax.set_ylabel('Casos') 
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}')) 
plt.tight_layout() 
plt.savefig('../02_graficas/g2_tendencia_anual.png', dpi=150) 
plt.close() 
print('g2 ok') 
 
# --- CONSUMO --- 
df_con = pd.read_excel('../01_datos/processed/p_salud_consumo.xlsx') 
df_con['loc'] = df_con['NOMBRELOCALIDADRESIDENCIA'].apply(norm) 
consumo_loc = df_con.groupby('loc')['CASOS'].sum().reset_index(name='consumo') 
 
# grafica 3: scatter ideacion vs consumo 
ideacion_loc = df_id.groupby('loc').size().reset_index(name='ideacion') 
merged = ideacion_loc.merge(consumo_loc, on='loc') 
fig, ax = plt.subplots(figsize=(9,6)) 
ax.scatter(merged['consumo'], merged['ideacion'], color='#D85A30', s=80, zorder=3) 
for _, row in merged.iterrows(): 
    ax.annotate(row['loc'], (row['consumo'], row['ideacion']), fontsize=7, ha='left', va='bottom') 
ax.set_xlabel('Casos consumo SPA') 
ax.set_ylabel('Casos ideacion suicida') 
ax.set_title('Ideacion suicida vs consumo SPA por localidad') 
plt.tight_layout() 
plt.savefig('../02_graficas/g3_ideacion_vs_consumo.png', dpi=150) 
plt.close() 
print('g3 ok') 
 
# --- DEPORTE --- 
df_dep = pd.read_excel('../01_datos/processed/p_programas_deporte.xlsx', header=1) 
df_dep.columns = [str(c).strip() for c in df_dep.columns] 
df_dep['loc'] = df_dep['Localidad'].apply(norm) 
deporte_loc = df_dep.groupby('loc')['Total'].sum().reset_index(name='participantes') 
merged2 = ideacion_loc.merge(deporte_loc, on='loc') 
fig, ax = plt.subplots(figsize=(9,6)) 
ax.scatter(merged2['participantes'], merged2['ideacion'], color='#1D9E75', s=80, zorder=3) 
for _, row in merged2.iterrows(): 
    ax.annotate(row['loc'], (row['participantes'], row['ideacion']), fontsize=7, ha='left', va='bottom') 
ax.set_xlabel('Participantes en programas deportivos') 
ax.set_ylabel('Casos ideacion suicida') 
ax.set_title('Ideacion suicida vs oferta deportiva por localidad') 
plt.tight_layout() 
plt.savefig('../02_graficas/g4_ideacion_vs_deporte.png', dpi=150) 
plt.close() 
print('g4 ok') 
print('Listo! Graficas en 02_graficas/') 
