import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import unicodedata, os
os.makedirs('../../02_graficas', exist_ok=True)

def norm(s):
    s = str(s).strip()
    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').upper()

poblacion = {
    'KENNEDY': 1200000, 'SUBA': 1400000, 'ENGATIVA': 900000,
    'BOSA': 800000, 'CIUDAD BOLIVAR': 750000, 'USAQUEN': 550000,
    'FONTIBON': 430000, 'SAN CRISTOBAL': 400000, 'CHAPINERO': 130000,
    'RAFAEL URIBE URIBE': 380000, 'USME': 430000, 'TUNJUELITO': 200000,
    'BARRIOS UNIDOS': 240000, 'TEUSAQUILLO': 150000, 'PUENTE ARANDA': 260000,
    'ANTONIO NARINO': 110000, 'LOS MARTIRES': 100000, 'SANTA FE': 110000,
    'LA CANDELARIA': 24000, 'SUMAPAZ': 6000,
}
pop_df = pd.DataFrame(list(poblacion.items()), columns=['loc','poblacion'])

print("Cargando datos...")
df_id  = pd.read_excel('../../01_datos/processed/p_salud_ideacion.xlsx')
df_hab = pd.read_excel('../../01_datos/processed/p_condiciones_habitabilidad.xlsx')

df_id['loc']  = df_id['localidad_residencia'].apply(norm)
df_hab['loc'] = df_hab['localidad'].apply(norm)
excluir = ['SIN DATO','','BOGOTA','LOCALIDAD DESCONOCIDA','SUMAPAZ']

factores = ['enfermedades_dolorosas','maltrato_sexual','muerte_familiar',
            'conflicto_pareja','problemas_economicos','problemas_juridicos',
            'problemas_laborales','suicidio_amigo']
factores_p = [f for f in factores if f in df_id.columns]

# ── PARTE 1: perfil del caso mas vulnerable ───────────────────────────────────
print("Calculando perfil de vulnerabilidad compuesta...")

# caso vulnerable: adolescente o joven + prob economicos + conflicto pareja
df_id['es_joven'] = df_id['ciclovital'].str.strip().isin([
    '12 - 17 Adolescencia','18 - 28 Juventud',
    '(12 a 17) Adolescencia','(18 a 28) Juventud'
]).astype(int)
df_id['es_intento'] = (df_id['clasificaciondelaconducta'].str.strip() == 'Intento de Suicidio').astype(int)
df_id['prob_eco'] = df_id['problemas_economicos'].fillna(0)
df_id['conf_par'] = df_id['conflicto_pareja'].fillna(0)
df_id['malt_sex'] = df_id['maltrato_sexual'].fillna(0)
df_id['n_factores'] = df_id[factores_p].sum(axis=1)

# score de vulnerabilidad por caso (0-5)
df_id['score_vuln'] = (
    df_id['es_joven'] +
    df_id['es_intento'] +
    df_id['prob_eco'] +
    df_id['conf_par'] +
    df_id['malt_sex']
)

# casos de maxima vulnerabilidad (score >= 3)
df_max_vuln = df_id[df_id['score_vuln'] >= 3]
vuln_loc = df_max_vuln.groupby('loc').size().reset_index(name='casos_alta_vuln')
total_loc = df_id.groupby('loc').size().reset_index(name='total')
vuln_pct = vuln_loc.merge(total_loc, on='loc')
vuln_pct['pct_alta_vuln'] = vuln_pct['casos_alta_vuln'] / vuln_pct['total'] * 100
vuln_pct = vuln_pct.merge(pop_df, on='loc', how='left')
vuln_pct['tasa_vuln_100k'] = vuln_pct['casos_alta_vuln'] / vuln_pct['poblacion'] * 100000
vuln_pct = vuln_pct[~vuln_pct['loc'].isin(excluir)].sort_values('tasa_vuln_100k', ascending=False)

print("\n=== CASOS DE ALTA VULNERABILIDAD POR LOCALIDAD ===")
print(vuln_pct[['loc','casos_alta_vuln','pct_alta_vuln','tasa_vuln_100k']].to_string(index=False))

# grafica h1: tasa de alta vulnerabilidad por localidad
fig, ax = plt.subplots(figsize=(12,6))
colores = ['#E24B4A' if v > vuln_pct['tasa_vuln_100k'].mean() else '#378ADD'
           for v in vuln_pct['tasa_vuln_100k']]
bars = ax.barh(vuln_pct['loc'], vuln_pct['tasa_vuln_100k'], color=colores, alpha=0.85)
ax.axvline(vuln_pct['tasa_vuln_100k'].mean(), color='gray', linestyle='--', linewidth=1,
           label=f'Promedio: {vuln_pct["tasa_vuln_100k"].mean():.0f}')
ax.set_xlabel('Casos de alta vulnerabilidad por 100.000 habitantes', fontsize=11)
ax.set_title('Concentracion de casos de maxima vulnerabilidad por localidad\n(joven + intento real + prob. economicos + conflicto pareja + maltrato)', fontsize=11)
ax.legend()
plt.tight_layout()
plt.savefig('../../02_graficas/h1_vulnerabilidad_compuesta.png', dpi=150)
plt.close()
print("h1 ok")

# grafica h2: scatter vulnerabilidad compuesta vs tasa de suicidio consumado
df_sui = pd.read_excel('../../01_datos/processed/p_salud_suicidio.xlsx')
df_sui['loc'] = df_sui['LOCALIDAD_DEL_HECHO'].apply(norm)
suicidio = df_sui[~df_sui['loc'].isin(excluir+['BOGOTA','LOCALIDAD DESCONOCIDA'])].groupby('loc').size().reset_index(name='suicidios')
df_h2 = vuln_pct.merge(suicidio, on='loc', how='left')
df_h2['tasa_suicidio'] = df_h2['suicidios'] / df_h2['poblacion'] * 100000
df_h2 = df_h2.dropna(subset=['tasa_suicidio'])

fig, ax = plt.subplots(figsize=(10,7))
sc = ax.scatter(df_h2['pct_alta_vuln'], df_h2['tasa_suicidio'],
                s=df_h2['casos_alta_vuln']/3, c=df_h2['tasa_vuln_100k'],
                cmap='YlOrRd', edgecolors='#444', linewidth=0.5, alpha=0.85, zorder=3)
for _, row in df_h2.iterrows():
    ax.annotate(row['loc'], (row['pct_alta_vuln'], row['tasa_suicidio']),
                fontsize=7.5, ha='left', va='bottom', color='#333')
coef = np.polyfit(df_h2['pct_alta_vuln'], df_h2['tasa_suicidio'], 1)
xline = np.linspace(df_h2['pct_alta_vuln'].min(), df_h2['pct_alta_vuln'].max(), 100)
ax.plot(xline, coef[0]*xline+coef[1], '--', color='gray', linewidth=1.5, label='Tendencia')
corr = df_h2['pct_alta_vuln'].corr(df_h2['tasa_suicidio'])
plt.colorbar(sc, ax=ax, label='Tasa vulnerabilidad por 100k hab')
ax.set_xlabel('% de casos con perfil de maxima vulnerabilidad', fontsize=11)
ax.set_ylabel('Tasa de suicidio consumado por 100.000 hab', fontsize=11)
ax.set_title(f'Vulnerabilidad compuesta vs suicidio consumado\n(correlacion r={corr:.2f} — el perfil vulnerable predice el suicidio?)', fontsize=11)
ax.legend()
plt.tight_layout()
plt.savefig('../../02_graficas/h2_vuln_vs_suicidio.png', dpi=150)
plt.close()
print("h2 ok")

# ── PARTE 2: habitabilidad + servicios vs tasa de intentos ───────────────────
print("\nProcesando regresion habitabilidad vs intentos...")

rezago = df_hab[df_hab['tipo_indicador'].str.strip()=='Rezago habitacional']
rezago_alto = rezago[rezago['categoria_indicador']=='Alto'].groupby('loc')['valor_indicador'].mean().reset_index(name='pct_rezago_alto')

servicios = df_hab[df_hab['tipo_indicador'].str.strip()=='Conexiones domiciliarias']
sin_serv = servicios[servicios['categoria_indicador']=='Sin servicios'].groupby('loc')['valor_indicador'].mean().reset_index(name='pct_sin_servicios')

superficie = df_hab[df_hab['tipo_indicador'].str.strip()=='Superficie por persona en vivienda']
superficie = superficie[superficie['valor_indicador'] < 200]
sup_loc = superficie.groupby('loc')['valor_indicador'].median().reset_index(name='m2_por_persona')

intento = df_id[df_id['clasificaciondelaconducta'].str.strip()=='Intento de Suicidio'].groupby('loc').size().reset_index(name='intentos')
df_hab2 = intento.merge(pop_df, on='loc', how='left')
df_hab2['tasa_intentos'] = df_hab2['intentos'] / df_hab2['poblacion'] * 100000
df_hab2 = df_hab2.merge(rezago_alto, on='loc', how='left')
df_hab2 = df_hab2.merge(sin_serv, on='loc', how='left')
df_hab2 = df_hab2.merge(sup_loc, on='loc', how='left')
df_hab2 = df_hab2[~df_hab2['loc'].isin(excluir)].dropna()

# normalizar indicadores habitabilidad
for col in ['pct_rezago_alto','pct_sin_servicios']:
    df_hab2[col+'_n'] = (df_hab2[col] - df_hab2[col].min()) / (df_hab2[col].max() - df_hab2[col].min())
df_hab2['m2_inv_n'] = 1 - (df_hab2['m2_por_persona'] - df_hab2['m2_por_persona'].min()) / (df_hab2['m2_por_persona'].max() - df_hab2['m2_por_persona'].min())
df_hab2['indice_habitabilidad'] = (df_hab2['pct_rezago_alto_n'] + df_hab2['pct_sin_servicios_n'] + df_hab2['m2_inv_n']) / 3

# grafica h3: indice habitabilidad vs tasa intentos
fig, ax = plt.subplots(figsize=(10,7))
sc = ax.scatter(df_hab2['indice_habitabilidad'], df_hab2['tasa_intentos'],
                s=df_hab2['poblacion']/8000, c=df_hab2['tasa_intentos'],
                cmap='YlOrRd', edgecolors='#444', linewidth=0.5, alpha=0.85, zorder=3)
for _, row in df_hab2.iterrows():
    ax.annotate(row['loc'], (row['indice_habitabilidad'], row['tasa_intentos']),
                fontsize=7.5, ha='left', va='bottom', color='#333')
coef3 = np.polyfit(df_hab2['indice_habitabilidad'], df_hab2['tasa_intentos'], 1)
xline3 = np.linspace(df_hab2['indice_habitabilidad'].min(), df_hab2['indice_habitabilidad'].max(), 100)
ax.plot(xline3, coef3[0]*xline3+coef3[1], '--', color='#E24B4A', linewidth=2, label='Tendencia')
corr3 = df_hab2['indice_habitabilidad'].corr(df_hab2['tasa_intentos'])
plt.colorbar(sc, ax=ax, label='Tasa intentos por 100k hab')
ax.set_xlabel('Indice de precariedad habitacional\n(rezago alto + sin servicios + hacinamiento)', fontsize=11)
ax.set_ylabel('Intentos de suicidio por 100.000 habitantes', fontsize=11)
ax.set_title(f'Precariedad habitacional vs intentos de suicidio per capita\n(correlacion r={corr3:.2f})', fontsize=12)
ax.legend()
plt.tight_layout()
plt.savefig('../../02_graficas/h3_habitabilidad_vs_intentos.png', dpi=150)
plt.close()
print("h3 ok")

# grafica h4: los 3 componentes en subplots lado a lado
fig, axes = plt.subplots(1,3, figsize=(16,6), sharey=True)
vars_x = ['pct_rezago_alto','pct_sin_servicios','m2_por_persona']
labels_x = ['% rezago habitacional alto','% viviendas sin servicios basicos','m² por persona (mediana)']
corrs_labels = []
for i, (ax, vx, lx) in enumerate(zip(axes, vars_x, labels_x)):
    corr_i = df_hab2[vx].corr(df_hab2['tasa_intentos'])
    corrs_labels.append(corr_i)
    color = '#E24B4A' if corr_i > 0 else '#378ADD'
    sc = ax.scatter(df_hab2[vx], df_hab2['tasa_intentos'],
                    s=df_hab2['poblacion']/10000, c=df_hab2['tasa_intentos'],
                    cmap='YlOrRd', edgecolors='#444', linewidth=0.4, alpha=0.85)
    for _, row in df_hab2.iterrows():
        ax.annotate(row['loc'], (row[vx], row['tasa_intentos']),
                    fontsize=6, ha='left', va='bottom', color='#555')
    coef_i = np.polyfit(df_hab2[vx], df_hab2['tasa_intentos'], 1)
    xl = np.linspace(df_hab2[vx].min(), df_hab2[vx].max(), 100)
    ax.plot(xl, coef_i[0]*xl+coef_i[1], '--', color=color, linewidth=1.5)
    ax.set_xlabel(lx, fontsize=9)
    ax.set_title(f'r = {corr_i:.2f}', fontsize=11, color=color)
    if i == 0:
        ax.set_ylabel('Intentos suicidio por 100k hab', fontsize=9)
fig.suptitle('Componentes de habitabilidad vs intentos de suicidio per capita', fontsize=13)
plt.tight_layout()
plt.savefig('../../02_graficas/h4_componentes_habitabilidad.png', dpi=150)
plt.close()
print("h4 ok")
print("\nTodo listo. 4 graficas en 02_graficas/")