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
 
df_id = pd.read_excel('../01_datos/processed/p_salud_ideacion.xlsx') 
df_id['loc'] = df_id['localidad_residencia'].apply(norm) 
ideacion = df_id.groupby('loc').size().reset_index(name='ideacion') 
 
df_con = pd.read_excel('../01_datos/processed/p_salud_consumo.xlsx') 
df_con['loc'] = df_con['NOMBRELOCALIDADRESIDENCIA'].apply(norm) 
consumo = df_con.groupby('loc')['CASOS'].sum().reset_index(name='consumo') 
 
df_dep = pd.read_excel('../01_datos/processed/p_programas_deporte.xlsx', header=2) 
df_dep.columns = [str(c).strip() for c in df_dep.columns] 
df_dep = df_dep[df_dep['Localidad'].notna()] 
df_dep['loc'] = df_dep['Localidad'].apply(norm) 
df_dep['Total'] = pd.to_numeric(df_dep['Total'], errors='coerce') 
deporte = df_dep.groupby('loc')['Total'].sum().reset_index(name='participantes_deporte') 
 
df_cc = pd.read_excel('../01_datos/processed/p_centros_culturales_bogota_limpio.xlsx') 
df_cc['loc'] = df_cc['Localidad'].apply(norm) 
culturales = df_cc.groupby('loc').size().reset_index(name='centros_culturales') 
 
df = ideacion.merge(consumo, on='loc', how='left') 
df = df.merge(deporte, on='loc', how='left') 
df = df.merge(culturales, on='loc', how='left') 
df = df.fillna(0) 
df = df[~df['loc'].isin(['SIN DATO',''])] 
print(df.to_string(index=False)) 
 
for col in ['ideacion','consumo','participantes_deporte','centros_culturales']: 
    df[col+'_n'] = (df[col]-df[col].min())/(df[col].max()-df[col].min()) 
df['riesgo'] = (df['ideacion_n'] + df['consumo_n']) / 2 
df['oferta'] = (df['participantes_deporte_n'] + df['centros_culturales_n']) / 2 
df['brecha'] = df['riesgo'] - df['oferta'] 
df = df.sort_values('brecha', ascending=False) 
 
fig, ax = plt.subplots(figsize=(11,7)) 
scatter = ax.scatter(df['oferta'], df['riesgo'], s=df['ideacion']/80, c=df['brecha'], cmap='RdYlGn_r', alpha=0.85, edgecolors='#444', linewidth=0.5, zorder=3) 
for _, row in df.iterrows(): 
    ax.annotate(row['loc'], (row['oferta'], row['riesgo']), fontsize=7.5, ha='left', va='bottom', color='#333') 
ax.axline((0,0), slope=1, color='gray', linestyle='--', linewidth=1, label='riesgo = oferta') 
ax.set_xlabel('Indice de oferta institucional (deporte + cultura)', fontsize=11) 
ax.set_ylabel('Indice de riesgo (ideacion + consumo SPA)', fontsize=11) 
ax.set_title('Brecha entre riesgo en salud mental y oferta institucional por localidad', fontsize=13) 
plt.colorbar(scatter, ax=ax, label='Brecha (riesgo - oferta)') 
ax.legend(fontsize=9) 
plt.tight_layout() 
plt.savefig('../02_graficas/g5_brecha_riesgo_oferta.png', dpi=150) 
plt.close() 
print('g5 ok') 
 
df2 = df.sort_values('ideacion', ascending=False).head(12) 
x = list(range(len(df2))) 
fig, ax = plt.subplots(figsize=(12,6)) 
ax.bar(x, df2['ideacion_n'], label='Ideacion suicida', color='#E24B4A', alpha=0.85) 
ax.bar(x, df2['consumo_n'], bottom=df2['ideacion_n'].values, label='Consumo SPA', color='#EF9F27', alpha=0.85) 
ax.bar(x, -df2['participantes_deporte_n'].values, label='Oferta deportiva', color='#1D9E75', alpha=0.85) 
ax.bar(x, -df2['centros_culturales_n'].values, bottom=-df2['participantes_deporte_n'].values, label='Centros culturales', color='#378ADD', alpha=0.85) 
ax.axhline(0, color='black', linewidth=0.8) 
ax.set_xticks(x) 
ax.set_xticklabels(list(df2['loc']), rotation=35, ha='right', fontsize=8) 
ax.set_ylabel('Indice normalizado (arriba=riesgo, abajo=oferta)') 
ax.set_title('Riesgo vs oferta institucional por localidad (top 12)', fontsize=12) 
ax.legend(fontsize=9) 
plt.tight_layout() 
plt.savefig('../02_graficas/g6_riesgo_vs_oferta_barras.png', dpi=150) 
plt.close() 
print('g6 ok') 
 
top5 = ideacion.sort_values('ideacion', ascending=False).head(5)['loc'].tolist() 
df_top = df_id[df_id['loc'].isin(top5)] 
tendencia = df_top.groupby(['ano_notificacion','loc']).size().reset_index(name='casos') 
colores = ['#E24B4A','#378ADD','#1D9E75','#EF9F27','#7F77DD'] 
fig, ax = plt.subplots(figsize=(11,6)) 
for i, loc in enumerate(top5): 
    d = tendencia[tendencia['loc']==loc] 
    ax.plot(d['ano_notificacion'], d['casos'], marker='o', label=loc, color=colores[i], linewidth=2) 
ax.set_title('Tendencia de ideacion suicida - top 5 localidades', fontsize=13) 
ax.set_xlabel('Ano') 
ax.set_ylabel('Casos') 
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}')) 
ax.legend(fontsize=9) 
plt.tight_layout() 
plt.savefig('../02_graficas/g7_tendencia_top5.png', dpi=150) 
plt.close() 
print('g7 ok') 
print('todo listo en 02_graficas/') 
