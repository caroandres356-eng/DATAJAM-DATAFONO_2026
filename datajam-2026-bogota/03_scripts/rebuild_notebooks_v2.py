"""
rebuild_notebooks_v2.py
Reconstruye los 6 notebooks usando CSV (carga rapida) y columnas verificadas.
"""
import json, os

NB_DIR = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\02_notebooks\Analisis_Andres"

KERNEL = {
    "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py", "mimetype": "text/x-python",
        "name": "python", "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3", "version": "3.14.3"
    }
}

def code_cell(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src}

def md_cell(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}

def save(path, cells):
    nb = {"cells": cells, "metadata": KERNEL, "nbformat": 4, "nbformat_minor": 5}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"  Guardado: {os.path.basename(path)}")

IMPORTS = (
    "import pandas as pd\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n"
    "import os\n"
)

# Bloque territorial reutilizable (recibe el nombre de variable del df y el string del nombre de columna)
def territorial_block(df_var, col_str, palette, title, head=10):
    col_repr = f"'{col_str}'" if not col_str.startswith("'") else col_str
    return (
        "# ── Estandarizacion por poblacion (tasa por 100k hab) ──────────────\n"
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "df_pob = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_poblacion_bogota.csv'))\n"
        "df_pob['localidad_clean'] = (\n"
        "    df_pob['localidad'].str.lower()\n"
        "    .str.normalize('NFKD')\n"
        "    .str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()\n"
        ")\n\n"
        f"_serie = {df_var}[{col_repr}].dropna().astype(str)\n"
        "_serie = (\n"
        "    _serie.str.lower()\n"
        "    .str.normalize('NFKD')\n"
        "    .str.encode('ascii', errors='ignore').str.decode('utf-8')\n"
        "    .str.replace(r'^\\d+\\s*-\\s*', '', regex=True).str.strip()\n"
        ")\n\n"
        "loc_counts = _serie.value_counts().rename_axis('localidad_clean').reset_index(name='casos')\n"
        "df_merged = loc_counts.merge(df_pob, on='localidad_clean', how='left')\n"
        "df_merged = df_merged[df_merged['poblacion'].notna() & (df_merged['poblacion'] > 0)].copy()\n"
        "df_merged['tasa_100k'] = (df_merged['casos'] / df_merged['poblacion']) * 100_000\n"
        f"df_merged = df_merged.sort_values('tasa_100k', ascending=False).head({head})\n\n"
        "plt.figure(figsize=(12, 6))\n"
        f"sns.barplot(x=df_merged['tasa_100k'], y=df_merged['localidad'], palette='{palette}')\n"
        f"plt.title('{title}')\n"
        "plt.xlabel('Tasa por 100,000 habitantes')\n"
        "plt.ylabel('Localidad')\n"
        "plt.tight_layout()\n"
        "plt.show()\n\n"
        "print('Top localidades (tasa relativa):')\n"
        "print(df_merged[['localidad', 'casos', 'poblacion', 'tasa_100k']].head(5).to_string(index=False))"
    )

# ══════════════════════════════════════════════════════════════════
# 01_Ideacion_Intento.ipynb   (254k filas — CSV es instant)
# col localidad: 'localidad_residencia'
# ══════════════════════════════════════════════════════════════════
cells_01 = [
    md_cell("# Salud: Ideacion / Intento (VARIABLE CENTRAL)\n\nEste es el corazon del analisis. Identificaremos localidades criticas, grupos poblacionales en riesgo y causas reportadas."),
    code_cell(IMPORTS + "\nsns.set_theme(style='whitegrid')\nplt.rcParams['figure.figsize'] = (10, 6)"),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "df_ideacion = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_salud_ideacion.csv'), encoding='utf-8-sig')\n"
        "print(f'Total de registros cargados: {len(df_ideacion):,}')\n"
        "print('Columnas:', df_ideacion.columns.tolist())\n"
        "display(df_ideacion.head())"
    ),
    md_cell("## Tendencia\n**Los casos aumentan por anio? Hay picos en ciertos anios?**"),
    code_cell(
        "col_ano = [c for c in df_ideacion.columns if 'ano' in c.lower() or 'year' in c.lower() or 'notif' in c.lower()]\n"
        "print('Columnas de anio encontradas:', col_ano)\n"
        "if col_ano:\n"
        "    _col = col_ano[0]\n"
        "    tendencia = df_ideacion[_col].value_counts().sort_index()\n"
        "    plt.figure(figsize=(10,5))\n"
        "    sns.lineplot(x=tendencia.index, y=tendencia.values, marker='o', linewidth=2.5)\n"
        "    plt.title('Tendencia Historica de Casos de Ideacion/Intento Suicida')\n"
        "    plt.xlabel('Anio')\n"
        "    plt.ylabel('Cantidad de Casos')\n"
        "    plt.tight_layout()\n"
        "    plt.show()\n"
        "else:\n"
        "    print('Columna de anio no encontrada. Columnas disponibles:', df_ideacion.columns.tolist())"
    ),
    md_cell("## Territorial (estandarizado por poblacion)\n**Que localidades tienen mayor TASA de casos respecto a sus habitantes?**"),
    code_cell(
        "col_loc = [c for c in df_ideacion.columns if 'localidad' in c.lower()]\n"
        "print('Columna de localidad detectada:', col_loc)\n"
        "if col_loc:\n"
        "    _col_loc = col_loc[0]\n"
        "    " + territorial_block("df_ideacion", "_col_loc", "Reds_r",
                                   "Tasa de Ideacion/Intento Suicida por 100k Habitantes", head=10).replace("\n", "\n    ")
    ),
    md_cell("## Perfil Poblacional\n**Que edades concentran mas casos? Diferencias por sexo?**"),
    code_cell(
        "col_edad = [c for c in df_ideacion.columns if 'edad' in c.lower()]\n"
        "col_sexo = [c for c in df_ideacion.columns if 'sexo' in c.lower()]\n"
        "print('edad:', col_edad, '| sexo:', col_sexo)\n"
        "if col_edad and col_sexo:\n"
        "    plt.figure(figsize=(12,6))\n"
        "    sns.histplot(data=df_ideacion, x=col_edad[0], hue=col_sexo[0], multiple='stack', bins=30, palette='Set2')\n"
        "    plt.title('Distribucion de Edades por Sexo en Ideacion Suicida')\n"
        "    plt.xlabel('Edad')\n"
        "    plt.ylabel('Frecuencia')\n"
        "    plt.show()\n"
        "    print(df_ideacion.groupby(col_sexo[0])[col_edad[0]].describe()[['count','mean','min','max']])"
    ),
    md_cell("## Factores asociados\n**Que variables o causas aparecen mas frecuentemente?**"),
    code_cell(
        "factores = ['enfermedades_dolorosas', 'maltrato_sexual', 'muerte_familiar',\n"
        "            'conflicto_pareja', 'problemas_economicos', 'esc_educ',\n"
        "            'problemas_juridicos', 'problemas_laborales', 'suicidio_amigo']\n"
        "factores_presentes = [f for f in factores if f in df_ideacion.columns]\n"
        "print('Factores encontrados:', factores_presentes)\n"
        "if factores_presentes:\n"
        "    conteos = df_ideacion[factores_presentes].apply(pd.to_numeric, errors='coerce').sum().sort_values(ascending=False)\n"
        "    plt.figure(figsize=(12,6))\n"
        "    sns.barplot(x=conteos.values, y=conteos.index, palette='rocket')\n"
        "    plt.title('Principales Factores Asociados a la Ideacion Suicida')\n"
        "    plt.xlabel('Numero de Reportes')\n"
        "    plt.ylabel('Factor de Riesgo')\n"
        "    plt.tight_layout()\n"
        "    plt.show()\n"
        "else:\n"
        "    print('Factores no detectados. Columnas disponibles:', df_ideacion.columns.tolist())"
    ),
]
save(os.path.join(NB_DIR, "01_Ideacion_Intento.ipynb"), cells_01)

# ══════════════════════════════════════════════════════════════════
# 02_Suicidio_Gravedad.ipynb
# cols: ANO_DEL_HECHO, LOCALIDAD_DEL_HECHO, GRUPO_DE_EDAD_QUINQUENAL_, SEXO_DE_LA_VICTIMA
# Normalizado a minusculas: ano_del_hecho, localidad_del_hecho, etc.
# ══════════════════════════════════════════════════════════════════
cells_02 = [
    md_cell("# Salud: Suicidio (RESULTADO MAS GRAVE)\n\nAnlisis para validar si los patrones de ideacion escalan a hechos consumados de forma proporcional."),
    code_cell(IMPORTS + "\nsns.set_theme(style='darkgrid')\nplt.rcParams['figure.figsize'] = (10, 6)"),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "df_suicidio = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_salud_suicidio.csv'), encoding='utf-8-sig')\n"
        "print(f'Total de registros cargados: {len(df_suicidio):,}')\n"
        "print('Columnas:', df_suicidio.columns.tolist())\n"
        "display(df_suicidio.head())"
    ),
    md_cell("## Tendencia\n**Tambien esta aumentando al igual que la ideacion?**"),
    code_cell(
        "col_ano = [c for c in df_suicidio.columns if 'ano' in c.lower() or 'year' in c.lower()]\n"
        "print('Columna de anio:', col_ano)\n"
        "if col_ano:\n"
        "    tendencia = df_suicidio[col_ano[0]].value_counts().sort_index()\n"
        "    plt.figure(figsize=(10,5))\n"
        "    sns.lineplot(x=tendencia.index, y=tendencia.values, marker='s', color='crimson', linewidth=2)\n"
        "    plt.title('Tendencia Historica de Suicidios Consumados')\n"
        "    plt.xlabel('Anio')\n"
        "    plt.ylabel('Cantidad de Casos')\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),
    md_cell("## Territorial (estandarizado por poblacion)\n**Coincide con las mismas localidades de ideacion? (Tasa por 100k)**"),
    code_cell(
        "col_loc = [c for c in df_suicidio.columns if 'localidad' in c.lower()]\n"
        "print('Columna de localidad:', col_loc)\n"
        "if col_loc:\n"
        "    _col_loc = col_loc[0]\n"
        "    " + territorial_block("df_suicidio", "_col_loc", "mako",
                                   "Tasa de Suicidios Consumados por 100k Habitantes", head=10).replace("\n", "\n    ")
    ),
    md_cell("## Perfil Demografico\n**Mismo grupo etario? Mismo sexo predominante?**"),
    code_cell(
        "col_edad = [c for c in df_suicidio.columns if 'edad' in c.lower() or 'quinquenal' in c.lower() or 'ciclo' in c.lower()]\n"
        "col_sexo = [c for c in df_suicidio.columns if 'sexo' in c.lower()]\n"
        "print('edad:', col_edad, '| sexo:', col_sexo)\n"
        "if col_edad and col_sexo:\n"
        "    plt.figure(figsize=(12,7))\n"
        "    orden = df_suicidio[col_edad[0]].value_counts().index\n"
        "    sns.countplot(data=df_suicidio, y=col_edad[0], hue=col_sexo[0], order=orden)\n"
        "    plt.title('Perfil Demografico: Edad y Sexo en Suicidios')\n"
        "    plt.xlabel('Numero de Casos')\n"
        "    plt.ylabel('Grupo de Edad')\n"
        "    plt.legend(title='Sexo')\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),
    md_cell("## Causas\n**Que razones o motivos de suicidio aparecen mas?**"),
    code_cell(
        "col_razon = [c for c in df_suicidio.columns if 'razon' in c.lower() or 'causa' in c.lower() or 'motivo' in c.lower()]\n"
        "print('Columna de razon:', col_razon)\n"
        "if col_razon:\n"
        "    razones = df_suicidio[col_razon[0]].value_counts().head(10)\n"
        "    plt.figure(figsize=(12,6))\n"
        "    sns.barplot(x=razones.values, y=razones.index, palette='flare')\n"
        "    plt.title('Principales Razones Reportadas de Suicidio')\n"
        "    plt.xlabel('Frecuencia')\n"
        "    plt.ylabel('Motivo')\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),
]
save(os.path.join(NB_DIR, "02_Suicidio_Gravedad.ipynb"), cells_02)

# ══════════════════════════════════════════════════════════════════
# 03_Contexto_Habitabilidad.ipynb
# cols: localidad, valor_indicador, clase_indicador, unidad_planeacion_zonal
# ══════════════════════════════════════════════════════════════════
cells_03 = [
    md_cell("# Habitabilidad / Accesibilidad (FACTOR TERRITORIAL)\n\nIdentificaremos las localidades con peores indicadores y armaremos un mapa de vulnerabilidad general."),
    code_cell(IMPORTS + "\nsns.set_theme(style='whitegrid')\nplt.rcParams['figure.figsize'] = (10, 6)"),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "df_habi = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_condiciones_habitabilidad.csv'), encoding='utf-8-sig')\n"
        "print(f'Total de registros cargados: {len(df_habi):,}')\n"
        "print('Columnas:', df_habi.columns.tolist())\n"
        "display(df_habi.head(3))"
    ),
    md_cell("## Territorial\n**Que localidades tienen peores indicadores? Ranking de vulnerabilidad**"),
    code_cell(
        "# Promedio del indicador — ya aislado de sesgo por tamano muestral\n"
        "if 'localidad' in df_habi.columns and 'valor_indicador' in df_habi.columns:\n"
        "    ranking_loc = (\n"
        "        df_habi.groupby('localidad')['valor_indicador']\n"
        "        .mean().sort_values(ascending=False).head(15)\n"
        "    )\n"
        "    plt.figure(figsize=(12,7))\n"
        "    sns.barplot(x=ranking_loc.values, y=ranking_loc.index, palette='magma')\n"
        "    plt.title('Promedio de Valor de Indicadores por Localidad (media)')\n"
        "    plt.xlabel('Valor Promedio del Indicador')\n"
        "    plt.ylabel('Localidad')\n"
        "    plt.tight_layout()\n"
        "    plt.show()\n"
        "else:\n"
        "    print('Columnas disponibles:', df_habi.columns.tolist())"
    ),
    md_cell("## Indicadores clave\n**Cuales indicadores son mas criticos?**"),
    code_cell(
        "col_clase = [c for c in df_habi.columns if 'clase' in c.lower() or 'tipo' in c.lower()]\n"
        "print('Columnas de clase/tipo:', col_clase)\n"
        "if col_clase:\n"
        "    top_ind = df_habi[col_clase[0]].value_counts().head(8)\n"
        "    plt.figure(figsize=(12,5))\n"
        "    sns.barplot(x=top_ind.values, y=top_ind.index, palette='viridis')\n"
        "    plt.title('Tipos de Indicadores con Mayor Frecuencia')\n"
        "    plt.xlabel('Frecuencia de Registro')\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),
    md_cell("## Distribucion por UPZ\n**Hay clusters de alta vulnerabilidad a nivel de UPZ?**"),
    code_cell(
        "col_upz = [c for c in df_habi.columns if 'upz' in c.lower() or 'planeacion' in c.lower()]\n"
        "print('Columna UPZ:', col_upz)\n"
        "if col_upz:\n"
        "    ranking_upz = df_habi[col_upz[0]].value_counts().head(10)\n"
        "    print('Top 10 UPZs con mayor frecuencia de registros:')\n"
        "    print(ranking_upz)"
    ),
]
save(os.path.join(NB_DIR, "03_Contexto_Habitabilidad.ipynb"), cells_03)

# ══════════════════════════════════════════════════════════════════
# 04_Oferta_Deporte.ipynb
# header=2 ya aplicado al CSV — col 'localidad' disponible
# ══════════════════════════════════════════════════════════════════
cells_04 = [
    md_cell("# Programas Deporte (OFERTA INSTITUCIONAL)\n\nRepresenta acceso a bienestar social y prevencion de conductas de riesgo."),
    code_cell(IMPORTS + "\nsns.set_theme(style='darkgrid')\nplt.rcParams['figure.figsize'] = (10, 6)"),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "df_deporte = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_programas_deporte.csv'), encoding='utf-8-sig')\n"
        "print(f'Total de registros cargados: {len(df_deporte):,}')\n"
        "print('Columnas:', df_deporte.columns.tolist())\n"
        "display(df_deporte.head(2))"
    ),
    md_cell("## Cobertura (estandarizada por poblacion)\n**En que localidades hay mas programas por habitante?**"),
    code_cell(
        "col_loc = [c for c in df_deporte.columns if 'localidad' in c.lower()]\n"
        "print('Columna de localidad:', col_loc)\n"
        "if col_loc:\n"
        "    _col_loc = col_loc[0]\n"
        "    " + territorial_block("df_deporte", "_col_loc", "crest",
                                   "Tasa de Cobertura Deportiva por 100k Habitantes", head=15).replace("\n", "\n    ") + "\n"
        "else:\n"
        "    print('No se detecto columna de localidad.')"
    ),
    md_cell("## Enfoque e Intensidad\n**Revision estadistica general de las variables disponibles**"),
    code_cell(
        "print('Revision estadistica rapida:')\n"
        "display(df_deporte.describe(include='all'))"
    ),
]
save(os.path.join(NB_DIR, "04_Oferta_Deporte.ipynb"), cells_04)

# ══════════════════════════════════════════════════════════════════
# 05_Oferta_Cultura.ipynb
# col: 'localidad' (con mayuscula en xlsx -> normalizado a minuscula en CSV)
# ══════════════════════════════════════════════════════════════════
cells_05 = [
    md_cell("# Centros Culturales (OTRA OFERTA INSTITUCIONAL)\n\nComplementa el deporte y muestra el mapa de acceso cultural de los jovenes."),
    code_cell(IMPORTS + "\nsns.set_theme(style='whitegrid')\nplt.rcParams['figure.figsize'] = (10, 6)"),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "df_cultura = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_centros_culturales_bogota_limpio.csv'), encoding='utf-8-sig')\n"
        "print(f'Total de registros cargados: {len(df_cultura):,}')\n"
        "print('Columnas:', df_cultura.columns.tolist())\n"
        "display(df_cultura.head(3))"
    ),
    md_cell("## Cobertura y Densidad (estandarizada por poblacion)\n**Cuantos centros culturales hay por cada 100k habitantes por localidad?**"),
    code_cell(
        "col_loc = [c for c in df_cultura.columns if 'localidad' in c.lower()]\n"
        "print('Columna de localidad:', col_loc)\n"
        "if col_loc:\n"
        "    _col_loc = col_loc[0]\n"
        "    " + territorial_block("df_cultura", "_col_loc", "husl",
                                   "Tasa de Centros Culturales por 100k Habitantes", head=20).replace("\n", "\n    ") + "\n"
        "else:\n"
        "    print('No se detecto columna de localidad.')"
    ),
    md_cell("## Distribucion\n**Hay zonas sin acceso? Lagunas culturales**"),
    code_cell(
        "col_loc = [c for c in df_cultura.columns if 'localidad' in c.lower()]\n"
        "if col_loc:\n"
        "    conteo = df_cultura[col_loc[0]].value_counts()\n"
        "    baja_cob = conteo[conteo <= 3]\n"
        "    print(f'Zonas con 3 o menos centros culturales ({len(baja_cob)} localidades):')\n"
        "    print(baja_cob)\n"
        "    col_upz = [c for c in df_cultura.columns if 'upz' in c.lower()]\n"
        "    if col_upz:\n"
        "        print(f'Total de UPZs impactadas: {df_cultura[col_upz[0]].nunique()} de 117 posibles.')"
    ),
]
save(os.path.join(NB_DIR, "05_Oferta_Cultura.ipynb"), cells_05)

# ══════════════════════════════════════════════════════════════════
# 06_Riesgo_Consumo_SPA.ipynb
# col localidad: 'nombrelocalidadresidencia'
# ══════════════════════════════════════════════════════════════════
cells_06 = [
    md_cell("# Salud: Consumo SPA (FACTOR DE RIESGO)\n\nIdentifica zonas y poblaciones con mayor riesgo de drogadiccion, co-factor de las ideaciones suicidas."),
    code_cell(IMPORTS + "\nsns.set_theme(style='whitegrid')\nplt.rcParams['figure.figsize'] = (10, 6)"),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "df_spa = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_salud_consumo.csv'), encoding='utf-8-sig')\n"
        "print(f'Total de registros cargados: {len(df_spa):,}')\n"
        "print('Columnas:', df_spa.columns.tolist())\n"
        "display(df_spa.head(3))"
    ),
    md_cell("## Tendencia\n**Aumenta el consumo historicamente?**"),
    code_cell(
        "col_ano = [c for c in df_spa.columns if 'ano' in c.lower() or 'year' in c.lower()]\n"
        "print('Columna de anio:', col_ano)\n"
        "if col_ano:\n"
        "    tendencia = df_spa[col_ano[0]].value_counts().sort_index()\n"
        "    plt.figure(figsize=(10,5))\n"
        "    sns.lineplot(x=tendencia.index, y=tendencia.values, marker='D', color='purple', linewidth=2)\n"
        "    plt.title('Curva Historica de Casos de Consumo SPA')\n"
        "    plt.xlabel('Anio')\n"
        "    plt.ylabel('Cantidad de Requerimientos')\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),
    md_cell("## Territorial (estandarizado por poblacion)\n**Donde es mas alta la tasa de consumo por habitante?**"),
    code_cell(
        "col_loc = [c for c in df_spa.columns if 'localidad' in c.lower()]\n"
        "print('Columna de localidad:', col_loc)\n"
        "if col_loc:\n"
        "    _col_loc = col_loc[0]\n"
        "    " + territorial_block("df_spa", "_col_loc", "inferno",
                                   "Tasa de Consumo SPA por 100k Habitantes", head=10).replace("\n", "\n    ") + "\n"
        "else:\n"
        "    print('No se detecto columna de localidad. Columnas disponibles:', df_spa.columns.tolist())"
    ),
    md_cell("## Contexto\n**Donde consumen (parques, vivienda, via publica)?**"),
    code_cell(
        "cols_contexto = [c for c in df_spa.columns if 'sitio' in c.lower()]\n"
        "print('Columnas de sitio:', cols_contexto)\n"
        "if cols_contexto:\n"
        "    df_ctx = df_spa[cols_contexto].apply(pd.to_numeric, errors='coerce').fillna(0)\n"
        "    sumas = df_ctx.sum().sort_values(ascending=False)\n"
        "    plt.figure(figsize=(12,6))\n"
        "    sns.barplot(x=sumas.values, y=sumas.index, palette='YlOrBr_r')\n"
        "    plt.title('Sitio Habitual de Consumo mas recurrente')\n"
        "    plt.xlabel('Veces Mencionado')\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),
    md_cell("## Perfil\n**Edad / ciclo de vida y Sexo predominante**"),
    code_cell(
        "col_vida = [c for c in df_spa.columns if 'curso' in c.lower() or 'ciclo' in c.lower() or 'vida' in c.lower()]\n"
        "col_sexo = [c for c in df_spa.columns if 'sexo' in c.lower()]\n"
        "print('curso_de_vida:', col_vida, '| sexo:', col_sexo)\n"
        "if col_vida and col_sexo:\n"
        "    plt.figure(figsize=(12,7))\n"
        "    orden = df_spa[col_vida[0]].value_counts().index\n"
        "    sns.countplot(data=df_spa, y=col_vida[0], hue=col_sexo[0], palette='pastel', order=orden)\n"
        "    plt.title('Distribucion de Consumidores por Curso de Vida y Sexo')\n"
        "    plt.xlabel('Volumen de Casos')\n"
        "    plt.ylabel('Curso de Vida')\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),
]
save(os.path.join(NB_DIR, "06_Riesgo_Consumo_SPA.ipynb"), cells_06)

print("Todos los notebooks reconstruidos correctamente.")
