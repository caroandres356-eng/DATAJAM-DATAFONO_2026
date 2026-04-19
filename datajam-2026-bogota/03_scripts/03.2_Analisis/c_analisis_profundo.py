import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import unicodedata, os
os.makedirs('../02_graficas', exist_ok=True)

def norm(s):
    s = str(s).strip()
    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').upper()

print("Cargando datos...")
df_id  = pd.read_excel('../01_datos/processed/p_salud_ideacion.xlsx')
df_con = pd.read_excel('../01_datos/processed/p_salud_consumo.xlsx')
df_dep = pd.read_excel('../01_datos/processed/p_programas_deporte.xlsx', header=2)
df_cc  = pd.read_excel('../01_datos/processed/p_centros_culturales_bogota_limpio.xlsx')

df_id['loc']  = df_id['localidad_residencia'].apply(norm)
df_con['loc'] = df_con['NOMBRELOCALIDADRESIDENCIA'].apply(norm)
df_dep.columns = [str(c).strip() for c in df_dep.columns]
df_dep = df_dep[df_dep['Localidad'].notna()]
df_dep['loc'] = df_dep['Localidad'].apply(norm)
df_dep['Total'] = pd.to_numeric(df_dep['Total'], errors='coerce')
df_cc['loc'] = df_cc['Localidad'].apply(norm)

ideacion   = df_id.groupby('loc').size().reset_index(name='ideacion')
consumo    = df_con.groupby('loc')['CASOS'].sum().reset_index(name='consumo')
deporte    = df_dep.groupby('loc')['Total'].sum().reset_index(name='participantes_deporte')
culturales = df_cc.groupby('loc').size().reset_index(name='centros_culturales')

df = ideacion.merge(consumo, on='loc', how='left')
df = df.merge(deporte, on='loc', how='left')
df = df.merge(culturales, on='loc', how='left')
df = df.fillna(0)
df = df[~df['loc'].isin(['SIN DATO',''])]

# �� METRICA 1: eficiencia de oferta ������������������������������������������
# casos de ideacion por cada 1000 participantes en deporte
df['ideacion_por_1k_deporte'] = (df['ideacion'] / df['participantes_deporte'].replace(0,1)) * 1000
df['ideacion_por_centro_cultural'] = (df['ideacion'] / df['centros_culturales'].replace(0,1))

print("\n=== EFICIENCIA DE OFERTA (ideacion por 1000 participantes deporte) ===")
print(df[['loc','ideacion','participantes_deporte','ideacion_por_1k_deporte']].sort_values('ideacion_por_1k_deporte', ascending=False).to_string(index=False))

fig, ax = plt.subplots(figsize=(11,6))
d = df.sort_values('ideacion_por_1k_deporte', ascending=True)
bars = ax.barh(d['loc'], d['ideacion_por_1k_deporte'], color='#E24B4A', alpha=0.85)
ax.axvline(d['ideacion_por_1k_deporte'].mean(), color='gray', linestyle='--', linewidth=1, label=f'Promedio: {d["ideacion_por_1k_deporte"].mean():.1f}')
ax.set_xlabel('Casos de ideacion por cada 1.000 participantes en deporte')
ax.set_title('Eficiencia de la oferta deportiva por localidad\n(alto = la oferta no alcanza para la demanda de riesgo)', fontsize=12)
ax.legend()
plt.tight_layout()
plt.savefig('../02_graficas/c1_eficiencia_oferta_deporte.png', dpi=150)
plt.close()
print("c1 ok")

# �� METRICA 2: perfil de vulnerabilidad por localidad ������������������������
factores = ['enfermedades_dolorosas','maltrato_sexual','muerte_familiar',
            'conflicto_pareja','problemas_economicos','problemas_juridicos',
            'problemas_laborales','suicidio_amigo']
factores_presentes = [f for f in factores if f in df_id.columns]

df_id_f = df_id[df_id['loc'].isin(df['loc'])]
perfil = df_id_f.groupby('loc')[factores_presentes].apply(lambda x: (x=='SI').sum())
perfil_pct = perfil.div(df_id_f.groupby('loc').size(), axis=0) * 100

print("\n=== PERFIL DE FACTORES DE RIESGO POR LOCALIDAD (% de casos) ===")
print(perfil_pct.round(1).to_string())

fig, ax = plt.subplots(figsize=(13,7))
im = ax.imshow(perfil_pct.T.values, aspect='auto', cmap='YlOrRd')
ax.set_xticks(range(len(perfil_pct.index)))
ax.set_xticklabels(perfil_pct.index, rotation=40, ha='right', fontsize=8)
ax.set_yticks(range(len(factores_presentes)))
ax.set_yticklabels([f.replace('_',' ') for f in factores_presentes], fontsize=9)
plt.colorbar(im, ax=ax, label='% de casos con este factor')
ax.set_title('Perfil de factores de riesgo por localidad\n(% de casos de ideacion que presentan cada factor)', fontsize=12)
plt.tight_layout()
plt.savefig('../02_graficas/c2_heatmap_factores_riesgo.png', dpi=150)
plt.close()
print("c2 ok")

# �� METRICA 3: co-ocurrencia de factores (acumulacion de riesgo) �������������
df_id['n_factores'] = df_id[factores_presentes].apply(lambda row: (row=='SI').sum(), axis=1)
cooc = df_id.groupby('loc')['n_factores'].mean().reset_index(name='promedio_factores')
cooc_dist = df_id.groupby(['loc','n_factores']).size().unstack(fill_value=0)

print("\n=== PROMEDIO DE FACTORES DE RIESGO SIMULTANEOS POR LOCALIDAD ===")
print(cooc.sort_values('promedio_factores', ascending=False).to_string(index=False))

fig, ax = plt.subplots(figsize=(11,6))
d = cooc.sort_values('promedio_factores', ascending=True)
ax.barh(d['loc'], d['promedio_factores'], color='#7F77DD', alpha=0.85)
ax.axvline(d['promedio_factores'].mean(), color='gray', linestyle='--', linewidth=1, label=f'Promedio ciudad: {d["promedio_factores"].mean():.2f}')
ax.set_xlabel('Promedio de factores de riesgo simultaneos por caso')
ax.set_title('Acumulacion de factores de riesgo por localidad\n(alto = los casos concentran multiples vulnerabilidades)', fontsize=12)
ax.legend()
plt.tight_layout()
plt.savefig('../02_graficas/c3_acumulacion_factores.png', dpi=150)
plt.close()
print("c3 ok")

# �� METRICA 4: evolucion pandemia por localidad �������������������������������
top8 = ideacion.sort_values('ideacion', ascending=False).head(8)['loc'].tolist()
df_top = df_id[df_id['loc'].isin(top8)]
tend = df_top.groupby(['ano_notificacion','loc']).size().reset_index(name='casos')

# calcular variacion 2019->2020 y 2020->2022
pivot = tend.pivot(index='ano_notificacion', columns='loc', values='casos').fillna(0)
print("\n=== EVOLUCION POR ANO (top 8 localidades) ===")
print(pivot.to_string())

fig, axes = plt.subplots(2,4, figsize=(16,8), sharey=False)
axes = axes.flatten()
colores = ['#E24B4A','#378ADD','#1D9E75','#EF9F27','#7F77DD','#D85A30','#1D9E75','#533AB7']
for i, loc in enumerate(top8):
    d = tend[tend['loc']==loc]
    axes[i].plot(d['ano_notificacion'], d['casos'], marker='o', color=colores[i], linewidth=2)
    axes[i].fill_between(d['ano_notificacion'], d['casos'], alpha=0.15, color=colores[i])
    axes[i].set_title(loc, fontsize=9, fontweight='bold')
    axes[i].axvspan(2019.5, 2020.5, alpha=0.08, color='red', label='pandemia')
    axes[i].set_xlabel('Ano', fontsize=8)
    axes[i].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}'))
fig.suptitle('Evolucion de ideacion suicida antes, durante y despues de pandemia\ntop 8 localidades', fontsize=13)
plt.tight_layout()
plt.savefig('../02_graficas/c4_evolucion_pandemia.png', dpi=150)
plt.close()
print("c4 ok")

# �� METRICA 5: consumo SPA como predictor territorial ������������������������
df_ratio = df.copy()
df_ratio['ratio_consumo_ideacion'] = df_ratio['consumo'] / df_ratio['ideacion'].replace(0,1)

print("\n=== RATIO CONSUMO/IDEACION POR LOCALIDAD ===")
print(df_ratio[['loc','consumo','ideacion','ratio_consumo_ideacion']].sort_values('ratio_consumo_ideacion', ascending=False).to_string(index=False))

fig, ax = plt.subplots(figsize=(11,6))
d = df_ratio.sort_values('ratio_consumo_ideacion', ascending=True)
colores_bar = ['#E24B4A' if v > d['ratio_consumo_ideacion'].mean() else '#378ADD' for v in d['ratio_consumo_ideacion']]
ax.barh(d['loc'], d['ratio_consumo_ideacion'], color=colores_bar, alpha=0.85)
ax.axvline(d['ratio_consumo_ideacion'].mean(), color='gray', linestyle='--', linewidth=1, label='Promedio')
ax.set_xlabel('Casos de consumo SPA por cada caso de ideacion suicida')
ax.set_title('Consumo SPA como predictor de riesgo territorial\n(rojo = sobre el promedio, mayor presion de consumo)', fontsize=12)
ax.legend()
plt.tight_layout()
plt.savefig('../02_graficas/c5_ratio_consumo_ideacion.png', dpi=150)
plt.close()
print("c5 ok")

# �� TABLA RESUMEN FINAL �������������������������������������������������������
resumen = df[['loc','ideacion','consumo','participantes_deporte','centros_culturales']].copy()
resumen = resumen.merge(cooc, on='loc', how='left')
resumen = resumen.merge(df_ratio[['loc','ratio_consumo_ideacion']], on='loc', how='left')
resumen = resumen.merge(df[['loc','ideacion_por_1k_deporte']], on='loc', how='left')
resumen = resumen.sort_values('ideacion', ascending=False)
resumen.to_excel('../01_datos/processed/p_tabla_resumen_localidades.xlsx', index=False)
print("\nTabla resumen guardada en processed/")
print("\nTodo listo. Graficas en 02_graficas/")

