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

# Poblacion aproximada por localidad Bogota (proyeccion 2023 DANE)
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
df_dep = pd.read_excel('../../01_datos/processed/p_programas_deporte.xlsx', header=2)
df_cc  = pd.read_excel('../../01_datos/processed/p_centros_culturales_bogota_limpio.xlsx')
df_sui = pd.read_excel('../../01_datos/processed/p_salud_suicidio.xlsx')

df_id['loc']  = df_id['localidad_residencia'].apply(norm)
df_dep.columns = [str(c).strip() for c in df_dep.columns]
df_dep = df_dep[df_dep['Localidad'].notna()]
df_dep['loc'] = df_dep['Localidad'].apply(norm)
df_dep['Total'] = pd.to_numeric(df_dep['Total'], errors='coerce')
df_cc['loc']  = df_cc['Localidad'].apply(norm)
df_sui['loc'] = df_sui['LOCALIDAD_DEL_HECHO'].apply(norm)

excluir = ['SIN DATO','','BOGOTA','LOCALIDAD DESCONOCIDA','SUMAPAZ']

# construir tabla maestra por localidad
ideacion = df_id.groupby('loc').size().reset_index(name='ideacion')
intento  = df_id[df_id['clasificaciondelaconducta'].str.strip()=='Intento de Suicidio'].groupby('loc').size().reset_index(name='intentos')
suicidio = df_sui[~df_sui['loc'].isin(excluir)].groupby('loc').size().reset_index(name='suicidios')
deporte  = df_dep[df_dep['MES']!='Total'].groupby('loc')['Total'].sum().reset_index(name='participantes_deporte')
culturales = df_cc.groupby('loc').size().reset_index(name='centros_culturales')

df = ideacion.merge(intento, on='loc', how='left')
df = df.merge(suicidio, on='loc', how='left')
df = df.merge(deporte, on='loc', how='left')
df = df.merge(culturales, on='loc', how='left')
df = df.merge(pop_df, on='loc', how='left')
df = df.fillna(0)
df = df[~df['loc'].isin(excluir)]
df = df[df['poblacion'] > 0]

# tasas por 100k habitantes
df['tasa_ideacion']  = df['ideacion']  / df['poblacion'] * 100000
df['tasa_intentos']  = df['intentos']  / df['poblacion'] * 100000
df['tasa_suicidio']  = df['suicidios'] / df['poblacion'] * 100000
df['oferta_deporte_per_cap'] = df['participantes_deporte'] / df['poblacion'] * 1000
df['centros_per_100k'] = df['centros_culturales'] / df['poblacion'] * 100000

print(df[['loc','tasa_ideacion','tasa_intentos','tasa_suicidio',
          'oferta_deporte_per_cap','centros_per_100k']].sort_values('tasa_intentos', ascending=False).to_string(index=False))

# ── GRAFICA 1: oferta deporte per capita vs tasa de intentos ─────────────────
fig, ax = plt.subplots(figsize=(10,7))
sc = ax.scatter(df['oferta_deporte_per_cap'], df['tasa_intentos'],
                s=df['poblacion']/8000, c=df['tasa_suicidio'],
                cmap='YlOrRd', edgecolors='#444', linewidth=0.5, alpha=0.85, zorder=3)
for _, row in df.iterrows():
    ax.annotate(row['loc'], (row['oferta_deporte_per_cap'], row['tasa_intentos']),
                fontsize=7.5, ha='left', va='bottom', color='#333')
coef = np.polyfit(df['oferta_deporte_per_cap'], df['tasa_intentos'], 1)
xline = np.linspace(df['oferta_deporte_per_cap'].min(), df['oferta_deporte_per_cap'].max(), 100)
ax.plot(xline, coef[0]*xline+coef[1], '--', color='gray', linewidth=1.5, label=f'Tendencia')
corr = df['oferta_deporte_per_cap'].corr(df['tasa_intentos'])
plt.colorbar(sc, ax=ax, label='Tasa suicidio consumado por 100k hab')
ax.set_xlabel('Participantes en deporte por cada 1.000 habitantes', fontsize=11)
ax.set_ylabel('Intentos de suicidio por cada 100.000 habitantes', fontsize=11)
ax.set_title(f'Oferta deportiva per capita vs tasa de intentos de suicidio\n(correlacion r={corr:.2f} | tamaño burbuja = poblacion)', fontsize=11)
ax.legend()
plt.tight_layout()
plt.savefig('../../02_graficas/g1_deporte_percap_vs_intentos.png', dpi=150)
plt.close()
print("g1 ok")

# ── GRAFICA 2: centros culturales per capita vs tasa de intentos ──────────────
fig, ax = plt.subplots(figsize=(10,7))
sc = ax.scatter(df['centros_per_100k'], df['tasa_intentos'],
                s=df['poblacion']/8000, c=df['tasa_suicidio'],
                cmap='YlOrRd', edgecolors='#444', linewidth=0.5, alpha=0.85, zorder=3)
for _, row in df.iterrows():
    ax.annotate(row['loc'], (row['centros_per_100k'], row['tasa_intentos']),
                fontsize=7.5, ha='left', va='bottom', color='#333')
coef2 = np.polyfit(df['centros_per_100k'], df['tasa_intentos'], 1)
xline2 = np.linspace(df['centros_per_100k'].min(), df['centros_per_100k'].max(), 100)
ax.plot(xline2, coef2[0]*xline2+coef2[1], '--', color='gray', linewidth=1.5, label='Tendencia')
corr2 = df['centros_per_100k'].corr(df['tasa_intentos'])
plt.colorbar(sc, ax=ax, label='Tasa suicidio consumado por 100k hab')
ax.set_xlabel('Centros culturales por cada 100.000 habitantes', fontsize=11)
ax.set_ylabel('Intentos de suicidio por cada 100.000 habitantes', fontsize=11)
ax.set_title(f'Centros culturales per capita vs tasa de intentos de suicidio\n(correlacion r={corr2:.2f} | tamaño burbuja = poblacion)', fontsize=11)
ax.legend()
plt.tight_layout()
plt.savefig('../../02_graficas/g2_cultura_percap_vs_intentos.png', dpi=150)
plt.close()
print("g2 ok")

# ── GRAFICA 3: indice combinado oferta vs tasa intentos ───────────────────────
df['oferta_n'] = (df['oferta_deporte_per_cap'] - df['oferta_deporte_per_cap'].min()) / (df['oferta_deporte_per_cap'].max() - df['oferta_deporte_per_cap'].min())
df['cultura_n'] = (df['centros_per_100k'] - df['centros_per_100k'].min()) / (df['centros_per_100k'].max() - df['centros_per_100k'].min())
df['indice_oferta'] = (df['oferta_n'] + df['cultura_n']) / 2

fig, ax = plt.subplots(figsize=(11,7))
sc = ax.scatter(df['indice_oferta'], df['tasa_intentos'],
                s=df['poblacion']/8000, c=df['tasa_suicidio'],
                cmap='YlOrRd', edgecolors='#444', linewidth=0.5, alpha=0.85, zorder=3)
for _, row in df.iterrows():
    ax.annotate(row['loc'], (row['indice_oferta'], row['tasa_intentos']),
                fontsize=7.5, ha='left', va='bottom', color='#333')
coef3 = np.polyfit(df['indice_oferta'], df['tasa_intentos'], 1)
xline3 = np.linspace(0, 1, 100)
ax.plot(xline3, coef3[0]*xline3+coef3[1], '--', color='#E24B4A', linewidth=2, label='Tendencia')
corr3 = df['indice_oferta'].corr(df['tasa_intentos'])
ax.axvline(df['indice_oferta'].mean(), color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax.axhline(df['tasa_intentos'].mean(), color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax.text(df['indice_oferta'].mean()+0.01, df['tasa_intentos'].max()*0.97,
        'Promedio oferta', fontsize=8, color='gray')
ax.text(0.01, df['tasa_intentos'].mean()+50, 'Promedio intentos', fontsize=8, color='gray')
plt.colorbar(sc, ax=ax, label='Tasa suicidio consumado por 100k hab')
ax.set_xlabel('Indice de oferta institucional (deporte + cultura) per capita', fontsize=11)
ax.set_ylabel('Intentos de suicidio por cada 100.000 habitantes', fontsize=11)
ax.set_title(f'Indice de oferta institucional vs intentos de suicidio per capita\n(correlacion r={corr3:.2f} — positivo significa mas oferta, mas intentos detectados?)', fontsize=10)
ax.legend()
plt.tight_layout()
plt.savefig('../../02_graficas/g3_indice_oferta_vs_intentos_percap.png', dpi=150)
plt.close()
print("g3 ok")

# ── GRAFICA 4: cuadrantes de riesgo e intervencion ───────────────────────────
df['riesgo_alto'] = df['tasa_intentos'] > df['tasa_intentos'].mean()
df['oferta_baja'] = df['indice_oferta'] < df['indice_oferta'].mean()

colores_cuad = {
    (True, True):  ('#E24B4A', 'Alto riesgo, baja oferta — URGENTE'),
    (True, False): ('#EF9F27', 'Alto riesgo, alta oferta — REFORZAR'),
    (False, True): ('#378ADD', 'Bajo riesgo, baja oferta — MONITOREAR'),
    (False, False):('#1D9E75', 'Bajo riesgo, alta oferta — MODELO'),
}

fig, ax = plt.subplots(figsize=(11,8))
for _, row in df.iterrows():
    key = (row['riesgo_alto'], row['oferta_baja'])
    color = colores_cuad[key][0]
    ax.scatter(row['indice_oferta'], row['tasa_intentos'],
               s=row['poblacion']/8000, c=color, edgecolors='#444',
               linewidth=0.5, alpha=0.85, zorder=3)
    ax.annotate(row['loc'], (row['indice_oferta'], row['tasa_intentos']),
                fontsize=7.5, ha='left', va='bottom', color='#333')

ax.axvline(df['indice_oferta'].mean(), color='gray', linestyle='--', linewidth=1.2)
ax.axhline(df['tasa_intentos'].mean(), color='gray', linestyle='--', linewidth=1.2)

for (r,o), (c, label) in colores_cuad.items():
    ax.scatter([], [], c=c, s=80, label=label)

ax.set_xlabel('Indice de oferta institucional per capita', fontsize=11)
ax.set_ylabel('Intentos de suicidio por 100.000 habitantes', fontsize=11)
ax.set_title('Mapa de cuadrantes: riesgo vs oferta institucional per capita\n(donde intervenir primero?)', fontsize=12)
ax.legend(fontsize=8, loc='upper right')
plt.tight_layout()
plt.savefig('../../02_graficas/g4_cuadrantes_riesgo_oferta.png', dpi=150)
plt.close()
print("g4 ok")
print("\nTodo listo.")