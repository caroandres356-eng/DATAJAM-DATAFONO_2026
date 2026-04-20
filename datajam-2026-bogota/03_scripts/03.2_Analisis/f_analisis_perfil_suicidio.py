import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import unicodedata, os, numpy as np
os.makedirs('../../02_graficas', exist_ok=True)

def norm(s):
    s = str(s).strip()
    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').upper()

print("Cargando datos...")
df_id  = pd.read_excel('../../01_datos/processed/p_salud_ideacion.xlsx')
df_sui = pd.read_excel('../../01_datos/processed/p_salud_suicidio.xlsx')
df_con = pd.read_excel('../../01_datos/processed/p_salud_consumo.xlsx')

df_id['loc'] = df_id['localidad_residencia'].apply(norm)
df_sui['loc'] = df_sui['LOCALIDAD_DEL_HECHO'].apply(norm)
df_con['loc'] = df_con['NOMBRELOCALIDADRESIDENCIA'].apply(norm)
excluir = ['SIN DATO','','BOGOTA','LOCALIDAD DESCONOCIDA']

# ── CRUCE 1: ideacion vs intento real por localidad ──────────────────────────
print("Procesando ideacion vs intento...")
df_id['conducta'] = df_id['clasificaciondelaconducta'].str.strip()
ideacion_pura = df_id[df_id['conducta']=='Ideación suicida'].groupby('loc').size().reset_index(name='ideacion_pura')
intento_real  = df_id[df_id['conducta']=='Intento de Suicidio'].groupby('loc').size().reset_index(name='intento_real')
df_conv = ideacion_pura.merge(intento_real, on='loc', how='inner')
df_conv = df_conv[~df_conv['loc'].isin(excluir)]
df_conv['ratio_intento'] = df_conv['intento_real'] / df_conv['ideacion_pura'] * 100
df_conv = df_conv.sort_values('ratio_intento', ascending=False)

fig, ax1 = plt.subplots(figsize=(13,6))
ax2 = ax1.twinx()
x = list(range(len(df_conv)))
colores = ['#E24B4A' if v > df_conv['ratio_intento'].mean() else '#378ADD' 
           for v in df_conv['ratio_intento']]
ax1.bar(x, df_conv['ratio_intento'], color=colores, alpha=0.85)
ax2.plot(x, df_conv['intento_real'], marker='o', color='black', linewidth=1.5, markersize=5)
ax1.axhline(df_conv['ratio_intento'].mean(), color='gray', linestyle='--', linewidth=1,
            label=f'Promedio: {df_conv["ratio_intento"].mean():.1f}%')
ax1.set_xticks(x)
ax1.set_xticklabels(df_conv['loc'], rotation=40, ha='right', fontsize=8)
ax1.set_ylabel('Intentos reales por cada 100 casos de ideacion', fontsize=10)
ax2.set_ylabel('Intentos reales (total)', fontsize=10)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'{int(v):,}'))
ax1.set_title('Tasa de intento real de suicidio por localidad\n(rojo = sobre el promedio, mayor urgencia de intervencion)', fontsize=12)
ax1.legend(fontsize=9)
plt.tight_layout()
plt.savefig('../../02_graficas/f1_intento_real_por_localidad.png', dpi=150)
plt.close()
print("f1 ok")
print(df_conv[['loc','ideacion_pura','intento_real','ratio_intento']].to_string(index=False))

# ── CRUCE 2: estacionalidad mensual del suicidio ─────────────────────────────
print("\nProcesando estacionalidad...")
meses_orden = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
               'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
mes_counts = df_sui['MES_DEL_HECHO'].str.strip().value_counts()
mes_vals = [mes_counts.get(m, 0) for m in meses_orden]

fig, ax = plt.subplots(figsize=(11,5))
colores_mes = ['#E24B4A' if v > np.mean(mes_vals) else '#378ADD' for v in mes_vals]
bars = ax.bar(meses_orden, mes_vals, color=colores_mes, alpha=0.85)
ax.axhline(np.mean(mes_vals), color='gray', linestyle='--', linewidth=1,
           label=f'Promedio mensual: {np.mean(mes_vals):.0f}')
for bar, val in zip(bars, mes_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            str(val), ha='center', fontsize=9)
ax.set_ylabel('Suicidios consumados')
ax.set_title('Estacionalidad del suicidio consumado en Bogota\n(rojo = sobre el promedio mensual)', fontsize=12)
ax.set_xticklabels(meses_orden, rotation=35, ha='right')
ax.legend()
plt.tight_layout()
plt.savefig('../../02_graficas/f2_estacionalidad_suicidio.png', dpi=150)
plt.close()
print("f2 ok")

# ── CRUCE 3: escolaridad vs razon del suicidio ───────────────────────────────
print("\nProcesando escolaridad vs razon...")
df_sui['escolaridad_clean'] = df_sui['ESCOLARIDAD'].str.strip()
df_sui['razon_clean'] = df_sui['RAZON_DEL_SUICIDIO'].str.strip()

esc_map = {
    'Educación inicial y educación preescolar': 'Preescolar',
    'Educación básica primaria': 'Primaria',
    'Básica primaria': 'Primaria',
    'Básica Primaria': 'Primaria',
    'Educación básica secundaria o secundaria baja': 'Secundaria',
    'Básica secundaria': 'Secundaria',
    'Educación media o secundaria alta': 'Media',
    'Educación técnica profesional y tecnológica': 'Técnica',
    'Tecnológica': 'Técnica',
    'Universitario': 'Universidad',
    'Profesional': 'Universidad',
    'Especialización, maestría o equivalente': 'Posgrado',
    'Especialización, Maestría o equivalente': 'Posgrado',
    'Doctorado o equivalente': 'Posgrado',
    'Sin escolaridad': 'Sin escolaridad',
    'Ninguna': 'Sin escolaridad',
}
df_sui['esc'] = df_sui['escolaridad_clean'].map(esc_map).fillna('Sin info')

razones_validas = ['Conflicto con pareja o ex-pareja','Económicas',
                   'Enfermedad física o mental','Enfermedad mental',
                   'Desamor','Sin información']
df_sui2 = df_sui[df_sui['razon_clean'].isin(razones_validas)]
esc_orden = ['Sin escolaridad','Primaria','Secundaria','Media','Técnica','Universidad','Posgrado']

pivot_esc = df_sui2.groupby(['esc','razon_clean']).size().unstack(fill_value=0)
pivot_esc = pivot_esc.reindex([e for e in esc_orden if e in pivot_esc.index])
pivot_esc_pct = pivot_esc.div(pivot_esc.sum(axis=1), axis=0) * 100

colores_razon = ['#E24B4A','#EF9F27','#1D9E75','#378ADD','#7F77DD','#D85A30']
fig, ax = plt.subplots(figsize=(12,6))
bottom = np.zeros(len(pivot_esc_pct))
for i, col in enumerate(pivot_esc_pct.columns):
    ax.bar(range(len(pivot_esc_pct)), pivot_esc_pct[col],
           bottom=bottom, label=col, color=colores_razon[i % len(colores_razon)], alpha=0.85)
    bottom += pivot_esc_pct[col].values
ax.set_xticks(range(len(pivot_esc_pct)))
ax.set_xticklabels(pivot_esc_pct.index, fontsize=10)
ax.set_ylabel('% de suicidios consumados por razon')
ax.set_title('Razon del suicidio consumado segun nivel educativo\n(a mayor educacion, cambia la razon del suicidio?)', fontsize=12)
ax.legend(fontsize=8, bbox_to_anchor=(1.01,1), loc='upper left')
plt.tight_layout()
plt.savefig('../../02_graficas/f3_escolaridad_vs_razon.png', dpi=150)
plt.close()
print("f3 ok")

# ── CRUCE 4: sitios de consumo SPA por localidad ─────────────────────────────
print("\nProcesando sitios de consumo...")
sitios = [c for c in df_con.columns if 'SITIO' in c]
sitios_labels = {
    'SITIOHABITUALCONSUMO_VIVIENDA': 'Vivienda',
    'SITIOHABITUALCONSUMO_PARQUE': 'Parque',
    'SITIOHABITUALCONSUMO_EST_EDUCATIVO': 'Est. Educativo',
    'SITIOHABITUALCONSUMO_BARES_TABERNAS': 'Bares/Tabernas',
    'SITIOHABITUALCONSUMO_VIA_PUBLICA': 'Via Publica',
    'SITIOHABITUALCONSUMO_CASA_AMIGOS': 'Casa Amigos',
}
for s in sitios:
    df_con[s] = df_con[s].astype(str).str.upper().str.strip()

df_con_loc = df_con[~df_con['loc'].isin(excluir)].copy()
sitio_loc = {}
for s in sitios:
    sitio_loc[sitios_labels[s]] = df_con_loc.groupby('loc').apply(
        lambda x: (x[s]=='SI').sum()
    )
df_sitios = pd.DataFrame(sitio_loc)
df_sitios = df_sitios.div(df_sitios.sum(axis=1), axis=0) * 100
df_sitios = df_sitios.loc[df_sitios.sum(axis=1).sort_values(ascending=False).head(15).index]

fig, ax = plt.subplots(figsize=(13,7))
bottom = np.zeros(len(df_sitios))
colores_sitio = ['#E24B4A','#1D9E75','#378ADD','#EF9F27','#7F77DD','#D85A30']
for i, col in enumerate(df_sitios.columns):
    ax.bar(range(len(df_sitios)), df_sitios[col],
           bottom=bottom, label=col, color=colores_sitio[i], alpha=0.85)
    bottom += df_sitios[col].values
ax.set_xticks(range(len(df_sitios)))
ax.set_xticklabels(df_sitios.index, rotation=40, ha='right', fontsize=8)
ax.set_ylabel('% de casos de consumo por sitio')
ax.set_title('Sitio habitual de consumo SPA por localidad\n(donde consume cada localidad?)', fontsize=12)
ax.legend(fontsize=9, bbox_to_anchor=(1.01,1), loc='upper left')
plt.tight_layout()
plt.savefig('../../02_graficas/f4_sitios_consumo_localidad.png', dpi=150)
plt.close()
print("f4 ok")

# ── CRUCE 5: solteros vs conflicto pareja en suicidio por localidad ──────────
print("\nProcesando estado civil vs localidad...")
df_sui['ec'] = df_sui['ESTADO_CIVIL'].str.strip().str.replace(' \(a\)','',regex=True).str.replace(' (a)','',regex=True)
ec_map = {'Soltero(a)':'Soltero','Soltero (a)':'Soltero',
          'Casado(a)':'Casado','Casado (a)':'Casado',
          'Viudo(a)':'Viudo','Viudo (a)':'Viudo',
          'Unión libre':'Union libre',
          'Separado(a), divorciado(a)':'Separado'}
df_sui['ec_clean'] = df_sui['ESTADO_CIVIL'].str.strip().map(ec_map).fillna('Sin info')

df_sui3 = df_sui[~df_sui['loc'].isin(excluir)]
pivot_ec = df_sui3.groupby(['loc','ec_clean']).size().unstack(fill_value=0)
pivot_ec = pivot_ec.loc[pivot_ec.sum(axis=1).sort_values(ascending=False).head(12).index]
pivot_ec_pct = pivot_ec.div(pivot_ec.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(13,6))
bottom = np.zeros(len(pivot_ec_pct))
colores_ec = ['#E24B4A','#378ADD','#1D9E75','#EF9F27','#7F77DD','#D85A30']
for i, col in enumerate(pivot_ec_pct.columns):
    ax.bar(range(len(pivot_ec_pct)), pivot_ec_pct[col],
           bottom=bottom, label=col, color=colores_ec[i % len(colores_ec)], alpha=0.85)
    bottom += pivot_ec_pct[col].values
ax.set_xticks(range(len(pivot_ec_pct)))
ax.set_xticklabels(pivot_ec_pct.index, rotation=40, ha='right', fontsize=8)
ax.set_ylabel('% de suicidios consumados por estado civil')
ax.set_title('Estado civil en suicidio consumado por localidad\n(solteros dominan en todas? o varia?)', fontsize=12)
ax.legend(fontsize=9, bbox_to_anchor=(1.01,1), loc='upper left')
plt.tight_layout()
plt.savefig('../../02_graficas/f5_estado_civil_suicidio.png', dpi=150)
plt.close()
print("f5 ok")
print("\nTodo listo. 5 graficas en 02_graficas/")