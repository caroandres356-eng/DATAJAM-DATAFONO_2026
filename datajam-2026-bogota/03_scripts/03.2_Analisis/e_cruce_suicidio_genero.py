import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import unicodedata, os, numpy as np
os.makedirs('../02_graficas', exist_ok=True)

def norm(s):
    s = str(s).strip()
    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').upper()

print("Cargando datos...")
df_id  = pd.read_excel('../01_datos/processed/p_salud_ideacion.xlsx')
df_sui = pd.read_excel('../01_datos/processed/p_salud_suicidio.xlsx')
df_con = pd.read_excel('../01_datos/processed/p_salud_consumo.xlsx')

df_id['loc']  = df_id['localidad_residencia'].apply(norm)
df_sui['loc'] = df_sui['LOCALIDAD_DEL_HECHO'].apply(norm)
df_con['loc'] = df_con['NOMBRELOCALIDADRESIDENCIA'].apply(norm)

excluir = ['SIN DATO','','BOGOTA','LOCALIDAD DESCONOCIDA']

# ── CRUCE 1: tasa de conversion ideacion → suicidio ──────────────────────────
print("Procesando tasa de conversion...")
ideacion = df_id.groupby('loc').size().reset_index(name='ideacion')
suicidio = df_sui[~df_sui['loc'].isin(excluir)].groupby('loc').size().reset_index(name='suicidios')
conv = ideacion.merge(suicidio, on='loc', how='inner')
conv = conv[~conv['loc'].isin(excluir)]
conv['tasa_conversion'] = (conv['suicidios'] / conv['ideacion']) * 100
conv = conv.sort_values('tasa_conversion', ascending=False)

fig, ax1 = plt.subplots(figsize=(12,6))
ax2 = ax1.twinx()
x = range(len(conv))
colores = ['#E24B4A' if v > conv['tasa_conversion'].mean() else '#378ADD' for v in conv['tasa_conversion']]
ax1.bar(x, conv['tasa_conversion'], color=colores, alpha=0.8, label='Tasa conversion (%)')
ax2.plot(x, conv['ideacion'], marker='o', color='#333', linewidth=1.5, markersize=5, label='Casos ideacion')
ax1.axhline(conv['tasa_conversion'].mean(), color='gray', linestyle='--', linewidth=1,
            label=f'Promedio: {conv["tasa_conversion"].mean():.2f}%')
ax1.set_xticks(list(x))
ax1.set_xticklabels(conv['loc'], rotation=40, ha='right', fontsize=8)
ax1.set_ylabel('Suicidios consumados por cada 100 casos de ideacion', fontsize=10)
ax2.set_ylabel('Casos de ideacion suicida', fontsize=10)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'{int(v):,}'))
ax1.set_title('Tasa de conversion ideacion → suicidio consumado por localidad\n(rojo = sobre el promedio, intervencion insuficiente)', fontsize=12)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, fontsize=8)
plt.tight_layout()
plt.savefig('../02_graficas/e1_tasa_conversion_suicidio.png', dpi=150)
plt.close()
print("e1 ok")
print(conv[['loc','ideacion','suicidios','tasa_conversion']].to_string(index=False))

# ── CRUCE 2: razon del suicidio por localidad ─────────────────────────────────
print("\nProcesando razones del suicidio...")
df_sui2 = df_sui[~df_sui['loc'].isin(excluir)].copy()
df_sui2['razon'] = df_sui2['RAZON_DEL_SUICIDIO'].str.strip()
razones_top = df_sui2['razon'].value_counts().head(6).index.tolist()
df_sui2 = df_sui2[df_sui2['razon'].isin(razones_top)]
pivot_razon = df_sui2.groupby(['loc','razon']).size().unstack(fill_value=0)
pivot_razon = pivot_razon.loc[pivot_razon.sum(axis=1).sort_values(ascending=False).head(14).index]
pivot_razon_pct = pivot_razon.div(pivot_razon.sum(axis=1), axis=0) * 100

colores_razon = ['#E24B4A','#378ADD','#EF9F27','#1D9E75','#7F77DD','#D85A30']
fig, ax = plt.subplots(figsize=(13,6))
bottom = np.zeros(len(pivot_razon_pct))
for i, razon in enumerate(pivot_razon_pct.columns):
    ax.bar(range(len(pivot_razon_pct)), pivot_razon_pct[razon],
           bottom=bottom, label=razon, color=colores_razon[i % len(colores_razon)], alpha=0.85)
    bottom += pivot_razon_pct[razon].values
ax.set_xticks(range(len(pivot_razon_pct)))
ax.set_xticklabels(pivot_razon_pct.index, rotation=40, ha='right', fontsize=8)
ax.set_ylabel('% de suicidios consumados por razon')
ax.set_title('Razon del suicidio consumado por localidad\n(composicion porcentual)', fontsize=12)
ax.legend(fontsize=8, bbox_to_anchor=(1.01,1), loc='upper left')
plt.tight_layout()
plt.savefig('../02_graficas/e2_razon_suicidio_localidad.png', dpi=150)
plt.close()
print("e2 ok")

# ── CRUCE 3: brecha de genero ideacion vs suicidio ────────────────────────────
print("\nProcesando brecha de genero...")
genero_id = df_id['sexo'].str.strip().str.upper().value_counts(normalize=True) * 100
genero_sui = df_sui['SEXO_DE_LA_VICTIMA'].str.strip().str.upper().value_counts(normalize=True) * 100
genero_con = df_con.groupby(df_con['SEXO'].str.strip().str.upper())['CASOS'].sum()
genero_con = genero_con / genero_con.sum() * 100

categorias = ['HOMBRE','MUJER']
id_vals  = [genero_id.get(c, 0) for c in categorias]
sui_vals = [genero_sui.get(c, 0) for c in categorias]
con_vals = [genero_con.get(c, 0) for c in categorias]

x = np.arange(len(categorias))
w = 0.25
fig, ax = plt.subplots(figsize=(9,6))
ax.bar(x-w, id_vals,  w, label='Ideacion suicida', color='#7F77DD', alpha=0.85)
ax.bar(x,   sui_vals, w, label='Suicidio consumado', color='#E24B4A', alpha=0.85)
ax.bar(x+w, con_vals, w, label='Consumo SPA', color='#EF9F27', alpha=0.85)
for i, (a,b,c) in enumerate(zip(id_vals, sui_vals, con_vals)):
    ax.text(i-w, a+0.5, f'{a:.1f}%', ha='center', fontsize=9)
    ax.text(i,   b+0.5, f'{b:.1f}%', ha='center', fontsize=9)
    ax.text(i+w, c+0.5, f'{c:.1f}%', ha='center', fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(categorias, fontsize=11)
ax.set_ylabel('% del total de casos')
ax.set_title('Brecha de genero: ideacion vs suicidio consumado vs consumo SPA\n(los hombres consuman mas, las mujeres ideacionan mas?)', fontsize=11)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('../02_graficas/e3_brecha_genero.png', dpi=150)
plt.close()
print("e3 ok")

# ── CRUCE 4: ciclo vital en ideacion vs suicidio consumado ───────────────────
print("\nProcesando ciclo vital...")
cv_id  = df_id['ciclovital'].str.strip().value_counts(normalize=True) * 100
cv_sui = df_sui['CICLO_VITAL'].str.strip().value_counts(normalize=True) * 100
cv_con = df_con.groupby('CURSO_DE_VIDA')['CASOS'].sum()
cv_con = cv_con / cv_con.sum() * 100

cv_orden = ['Primera Infancia','Infancia','Adolescencia','Juventud','Adultez','Vejez',
            'Persona Mayor','(12 a 17) Adolescencia','(18 a 28) Juventud',
            '(29 a 59) Adultez','(60 o mas) Persona Mayor']

fig, axes = plt.subplots(1,3, figsize=(15,6))
for ax, data, titulo, color in zip(axes,
    [cv_id, cv_sui, cv_con],
    ['Ideacion suicida','Suicidio consumado','Consumo SPA'],
    ['#7F77DD','#E24B4A','#EF9F27']):
    d = data.sort_values(ascending=True)
    ax.barh(d.index, d.values, color=color, alpha=0.85)
    ax.set_xlabel('% del total')
    ax.set_title(titulo, fontsize=11)
    for i, v in enumerate(d.values):
        ax.text(v+0.3, i, f'{v:.1f}%', va='center', fontsize=8)
fig.suptitle('Distribucion por ciclo vital: ideacion vs suicidio vs consumo SPA', fontsize=13)
plt.tight_layout()
plt.savefig('../02_graficas/e4_ciclo_vital_comparado.png', dpi=150)
plt.close()
print("e4 ok")
print("\nTodo listo.")
