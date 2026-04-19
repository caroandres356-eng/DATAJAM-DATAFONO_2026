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
df_hab = pd.read_excel('../01_datos/processed/p_condiciones_habitabilidad.xlsx')

df_id['loc'] = df_id['localidad_residencia'].apply(norm)
df_hab['loc'] = df_hab['localidad'].apply(norm)

ideacion = df_id.groupby('loc').size().reset_index(name='ideacion')
factores = ['enfermedades_dolorosas','maltrato_sexual','muerte_familiar',
            'conflicto_pareja','problemas_economicos','problemas_juridicos',
            'problemas_laborales','suicidio_amigo']
factores_p = [f for f in factores if f in df_id.columns]
df_id['n_factores'] = df_id[factores_p].sum(axis=1)
prob_eco = df_id.groupby('loc')['problemas_economicos'].mean().reset_index(name='pct_prob_economico')

# ── CRUCE 1: estrato vs ideacion ─────────────────────────────────────────────
print("Procesando estrato vs ideacion...")
estrato = df_hab[df_hab['tipo_indicador'].str.strip()=='Estructuras Durables'].copy()
estrato = estrato[estrato['categoria_secundaria_indicador'].str.contains('Estrato', na=False)]
estrato['estrato'] = estrato['categoria_secundaria_indicador'].str.strip()
estrato_loc = estrato.groupby(['loc','estrato'])['valor_indicador'].mean().reset_index()

estratos_orden = ['Estrato 1','Estrato 2','Estrato 3','Estrato 4','Estrato 5','Estrato 6']
pivot_est = estrato_loc.pivot_table(index='loc', columns='estrato', values='valor_indicador').fillna(0)
pivot_est = pivot_est.merge(ideacion, on='loc')
pivot_est = pivot_est.sort_values('ideacion', ascending=False).head(15)

fig, ax1 = plt.subplots(figsize=(13,6))
ax2 = ax1.twinx()
bottom = None
colores_est = ['#E24B4A','#EF9F27','#FAC775','#9FE1CB','#378ADD','#0C447C']
x = range(len(pivot_est))
for i, est in enumerate([e for e in estratos_orden if e in pivot_est.columns]):
    vals = pivot_est[est].values
    if bottom is None:
        ax1.bar(x, vals, label=est, color=colores_est[i], alpha=0.75)
        bottom = vals.copy()
    else:
        ax1.bar(x, vals, bottom=bottom, label=est, color=colores_est[i], alpha=0.75)
        bottom += vals
ax2.plot(x, pivot_est['ideacion'].values, marker='o', color='black', linewidth=2, label='Casos ideacion')
ax1.set_xticks(list(x))
ax1.set_xticklabels(pivot_est['loc'].values, rotation=35, ha='right', fontsize=8)
ax1.set_ylabel('% estructuras durables por estrato')
ax2.set_ylabel('Casos de ideacion suicida')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'{int(v):,}'))
ax1.set_title('Composicion de estrato socioeconomico vs ideacion suicida por localidad', fontsize=12)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, fontsize=8, loc='upper right')
plt.tight_layout()
plt.savefig('../02_graficas/d1_estrato_vs_ideacion.png', dpi=150)
plt.close()
print("d1 ok")

# ── CRUCE 2: rezago habitacional alto vs ideacion ─────────────────────────────
print("Procesando rezago habitacional...")
rezago = df_hab[df_hab['tipo_indicador'].str.strip()=='Rezago habitacional'].copy()
rezago_alto = rezago[rezago['categoria_indicador']=='Alto'].groupby('loc')['valor_indicador'].mean().reset_index(name='pct_rezago_alto')
df2 = ideacion.merge(rezago_alto, on='loc', how='inner')
df2 = df2[~df2['loc'].isin(['SIN DATO',''])]

fig, ax = plt.subplots(figsize=(10,6))
sc = ax.scatter(df2['pct_rezago_alto'], df2['ideacion'],
                s=120, c=df2['ideacion'], cmap='YlOrRd', edgecolors='#444', linewidth=0.5, zorder=3)
for _, row in df2.iterrows():
    ax.annotate(row['loc'], (row['pct_rezago_alto'], row['ideacion']),
                fontsize=7.5, ha='left', va='bottom', color='#333')
z = df2[['pct_rezago_alto','ideacion']].dropna()
m, b = pd.Series(z['ideacion']).values, pd.Series(z['pct_rezago_alto']).values
import numpy as np
coef = np.polyfit(b, m, 1)
xline = np.linspace(b.min(), b.max(), 100)
ax.plot(xline, coef[0]*xline+coef[1], '--', color='gray', linewidth=1.2, label=f'Tendencia')
plt.colorbar(sc, ax=ax, label='Casos ideacion')
ax.set_xlabel('% viviendas con rezago habitacional ALTO', fontsize=11)
ax.set_ylabel('Casos de ideacion suicida', fontsize=11)
ax.set_title('Rezago habitacional alto vs ideacion suicida por localidad\n(cada punto = una localidad)', fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'{int(v):,}'))
ax.legend()
plt.tight_layout()
plt.savefig('../02_graficas/d2_rezago_vs_ideacion.png', dpi=150)
plt.close()
print("d2 ok")

# ── CRUCE 3: sin servicios basicos vs ideacion ────────────────────────────────
print("Procesando servicios basicos...")
servicios = df_hab[df_hab['tipo_indicador'].str.strip()=='Conexiones domiciliarias'].copy()
sin_serv = servicios[servicios['categoria_indicador']=='Sin servicios'].groupby('loc')['valor_indicador'].mean().reset_index(name='pct_sin_servicios')
df3 = ideacion.merge(sin_serv, on='loc', how='inner')
df3 = df3[~df3['loc'].isin(['SIN DATO',''])]

fig, ax = plt.subplots(figsize=(10,6))
sc = ax.scatter(df3['pct_sin_servicios'], df3['ideacion'],
                s=120, c=df3['ideacion'], cmap='YlOrRd', edgecolors='#444', linewidth=0.5, zorder=3)
for _, row in df3.iterrows():
    ax.annotate(row['loc'], (row['pct_sin_servicios'], row['ideacion']),
                fontsize=7.5, ha='left', va='bottom', color='#333')
z2 = df3[['pct_sin_servicios','ideacion']].dropna()
coef2 = np.polyfit(z2['pct_sin_servicios'], z2['ideacion'], 1)
xline2 = np.linspace(z2['pct_sin_servicios'].min(), z2['pct_sin_servicios'].max(), 100)
ax.plot(xline2, coef2[0]*xline2+coef2[1], '--', color='gray', linewidth=1.2, label='Tendencia')
plt.colorbar(sc, ax=ax, label='Casos ideacion')
ax.set_xlabel('% viviendas sin servicios basicos', fontsize=11)
ax.set_ylabel('Casos de ideacion suicida', fontsize=11)
ax.set_title('Acceso a servicios basicos vs ideacion suicida por localidad', fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'{int(v):,}'))
ax.legend()
plt.tight_layout()
plt.savefig('../02_graficas/d3_servicios_vs_ideacion.png', dpi=150)
plt.close()
print("d3 ok")

# ── CRUCE 4: superficie por persona vs problemas economicos ──────────────────
print("Procesando superficie por persona...")
superficie = df_hab[df_hab['tipo_indicador'].str.strip()=='Superficie por persona en vivienda'].copy()
superficie = superficie[superficie['valor_indicador'] < 200]
sup_loc = superficie.groupby('loc')['valor_indicador'].median().reset_index(name='m2_por_persona')
df4 = prob_eco.merge(sup_loc, on='loc', how='inner')
df4 = df4.merge(ideacion, on='loc', how='inner')
df4 = df4[~df4['loc'].isin(['SIN DATO',''])]

fig, ax = plt.subplots(figsize=(10,6))
sc = ax.scatter(df4['m2_por_persona'], df4['pct_prob_economico']*100,
                s=df4['ideacion']/50, c=df4['ideacion'], cmap='YlOrRd',
                edgecolors='#444', linewidth=0.5, alpha=0.85, zorder=3)
for _, row in df4.iterrows():
    ax.annotate(row['loc'], (row['m2_por_persona'], row['pct_prob_economico']*100),
                fontsize=7.5, ha='left', va='bottom', color='#333')
plt.colorbar(sc, ax=ax, label='Casos ideacion (tamaño burbuja)')
ax.set_xlabel('Mediana m² por persona en vivienda', fontsize=11)
ax.set_ylabel('% casos con problemas economicos', fontsize=11)
ax.set_title('Hacinamiento (m² por persona) vs problemas economicos en casos de ideacion\n(tamaño burbuja = total casos)', fontsize=11)
plt.tight_layout()
plt.savefig('../02_graficas/d4_hacinamiento_vs_prob_economico.png', dpi=150)
plt.close()
print("d4 ok")

# ── CRUCE 5: vivienda en zona de riesgo vs ideacion ──────────────────────────
print("Procesando zona de riesgo...")
riesgo_viv = df_hab[df_hab['tipo_indicador'].str.strip()=='Vivienda en ubicación sujeta a riesgo'].copy()
riesgo_loc = riesgo_viv.groupby('loc')['valor_indicador'].mean().reset_index(name='pct_zona_riesgo')
df5 = ideacion.merge(riesgo_loc, on='loc', how='inner')
df5 = df5.merge(prob_eco, on='loc', how='inner')
df5 = df5[~df5['loc'].isin(['SIN DATO',''])]

fig, ax = plt.subplots(figsize=(10,6))
sc = ax.scatter(df5['pct_zona_riesgo'], df5['ideacion'],
                s=df5['pct_prob_economico']*800, c=df5['pct_prob_economico'],
                cmap='RdYlGn_r', edgecolors='#444', linewidth=0.5, alpha=0.85, zorder=3)
for _, row in df5.iterrows():
    ax.annotate(row['loc'], (row['pct_zona_riesgo'], row['ideacion']),
                fontsize=7.5, ha='left', va='bottom', color='#333')
plt.colorbar(sc, ax=ax, label='% casos con problemas economicos')
ax.set_xlabel('% viviendas en zona sujeta a riesgo', fontsize=11)
ax.set_ylabel('Casos de ideacion suicida', fontsize=11)
ax.set_title('Vivienda en zona de riesgo vs ideacion suicida\n(tamaño y color = presion de problemas economicos)', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'{int(v):,}'))
plt.tight_layout()
plt.savefig('../02_graficas/d5_zona_riesgo_vs_ideacion.png', dpi=150)
plt.close()
print("d5 ok")
print("\nTodo listo. 5 graficas en 02_graficas/")
