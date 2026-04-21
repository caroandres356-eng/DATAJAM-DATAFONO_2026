"""
rebuild_notebooks.py
Reescribe COMPLETAMENTE las celdas territoriales de los 5 notebooks afectados.
"""
import json, os

NB_DIR = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\02_notebooks\Analisis_Andres"

KERNEL = {
    "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbformat": 4,
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.14.3"
    }
}

def code_cell(source: str):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": source}

def md_cell(source: str):
    return {"cell_type": "markdown", "metadata": {}, "source": source}

def save(path, cells):
    nb = {"cells": cells, "metadata": KERNEL, "nbformat": 4, "nbformat_minor": 5}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"  Guardado: {os.path.basename(path)}")

# ------------------------------------------------------------------
# Bloque reutilizable de normalización territorial
# ------------------------------------------------------------------
def territorial_block(df_var, col_expr, palette, title, head=10):
    return (
        f"# ── Estandarización por población (tasa por 100k hab) ──────────────\n"
        f"PROCESSED_DIR = '../../01_datos/processed'\n"
        f"df_pob = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_poblacion_bogota.csv'))\n"
        f"df_pob['localidad_clean'] = (\n"
        f"    df_pob['localidad'].str.lower()\n"
        f"    .str.normalize('NFKD')\n"
        f"    .str.encode('ascii', errors='ignore').str.decode('utf-8')\n"
        f")\n\n"
        f"# Limpiar y normalizar la columna de localidad del dataset\n"
        f"_serie = {df_var}[{col_expr}].dropna().astype(str)\n"
        f"_serie = (\n"
        f"    _serie.str.lower()\n"
        f"    .str.normalize('NFKD')\n"
        f"    .str.encode('ascii', errors='ignore').str.decode('utf-8')\n"
        f"    .str.replace(r'^\\d+\\s*-\\s*', '', regex=True).str.strip()\n"
        f")\n\n"
        f"# Conteo y merge con población\n"
        f"loc_counts = _serie.value_counts().rename_axis('localidad_clean').reset_index(name='casos')\n"
        f"df_merged = loc_counts.merge(df_pob, on='localidad_clean', how='left')\n"
        f"df_merged = df_merged[df_merged['poblacion'].notna() & (df_merged['poblacion'] > 0)].copy()\n\n"
        f"# Tasa por 100,000 habitantes\n"
        f"df_merged['tasa_100k'] = (df_merged['casos'] / df_merged['poblacion']) * 100_000\n"
        f"df_merged = df_merged.sort_values('tasa_100k', ascending=False).head({head})\n\n"
        f"# Gráfico\n"
        f"plt.figure(figsize=(12, 6))\n"
        f"sns.barplot(x=df_merged['tasa_100k'], y=df_merged['localidad'], palette='{palette}')\n"
        f"plt.title('{title}')\n"
        f"plt.xlabel('Tasa por 100,000 habitantes')\n"
        f"plt.ylabel('Localidad')\n"
        f"plt.tight_layout()\n"
        f"plt.show()\n\n"
        f"print('Top localidades (tasa relativa):')\n"
        f"print(df_merged[['localidad', 'casos', 'poblacion', 'tasa_100k']].head(5).to_string(index=False))"
    )

# ══════════════════════════════════════════════════════════════════
# 01_Ideacion_Intento.ipynb
# ══════════════════════════════════════════════════════════════════
cells_01 = [
    md_cell("# 🧠 1. Salud: Ideación / Intento (VARIABLE CENTRAL)\n\n👉 Este es el corazón del análisis. Identificaremos localidades críticas, grupos poblacionales en riesgo y causas reportadas."),
    code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "import os\n\n"
        "sns.set_theme(style='whitegrid')\n"
        "plt.rcParams['figure.figsize'] = (10, 6)"
    ),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "file_path = os.path.join(PROCESSED_DIR, 'p_salud_ideacion.xlsx')\n"
        "df_ideacion = pd.read_excel(file_path)\n"
        "print(f'Total de registros cargados: {len(df_ideacion):,}')\n"
        "display(df_ideacion.head())"
    ),
    md_cell("## 📈 Tendencia\n**¿Los casos aumentan por año? ¿Hay picos en ciertos años?**"),
    code_cell(
        "if 'ano_notificacion' in df_ideacion.columns:\n"
        "    tendencia = df_ideacion['ano_notificacion'].value_counts().sort_index()\n"
        "    plt.figure(figsize=(10,5))\n"
        "    sns.lineplot(x=tendencia.index, y=tendencia.values, marker='o', linewidth=2.5)\n"
        "    plt.title('Tendencia Histórica de Casos de Ideación/Intento Suicida')\n"
        "    plt.xlabel('Año')\n"
        "    plt.ylabel('Cantidad de Casos')\n"
        "    plt.xticks(tendencia.index)\n"
        "    plt.show()\n"
        "else:\n"
        "    print('Columna de año no encontrada.')"
    ),
    md_cell("## 📍 Territorial (estandarizado por población)\n**¿Qué localidades tienen mayor TASA de casos relative a sus habitantes?**"),
    code_cell(territorial_block(
        "df_ideacion", "'localidad_residencia'",
        "Reds_r", "Tasa de Ideación/Intento Suicida por 100k Habitantes", head=10
    )),
    md_cell("## 👥 Perfil Poblacional\n**¿Qué edades concentran más casos? ¿Diferencias por sexo?**"),
    code_cell(
        "if 'edad' in df_ideacion.columns and 'sexo' in df_ideacion.columns:\n"
        "    plt.figure(figsize=(12,6))\n"
        "    sns.histplot(data=df_ideacion, x='edad', hue='sexo', multiple='stack', bins=30, palette='Set2')\n"
        "    plt.title('Distribución de Edades por Sexo en Ideación Suicida')\n"
        "    plt.xlabel('Edad')\n"
        "    plt.ylabel('Frecuencia')\n"
        "    plt.show()\n\n"
        "    print('Análisis Rápido Edad/Sexo:')\n"
        "    print(df_ideacion.groupby('sexo')['edad'].describe()[['count', 'mean', 'min', 'max']])"
    ),
    md_cell("## ⚠️ Factores asociados\n**¿Qué variables o causas aparecen más frecuentemente?**"),
    code_cell(
        "factores = ['enfermedades_dolorosas', 'maltrato_sexual', 'muerte_familiar',\n"
        "            'conflicto_pareja', 'problemas_economicos', 'esc_educ',\n"
        "            'problemas_juridicos', 'problemas_laborales', 'suicidio_amigo']\n\n"
        "factores_presentes = [f for f in factores if f in df_ideacion.columns]\n"
        "if factores_presentes:\n"
        "    conteos = df_ideacion[factores_presentes].sum().sort_values(ascending=False)\n"
        "    plt.figure(figsize=(12,6))\n"
        "    sns.barplot(x=conteos.values, y=conteos.index, palette='rocket')\n"
        "    plt.title('Principales Factores Asociados a la Ideación Suicida')\n"
        "    plt.xlabel('Número de Reportes')\n"
        "    plt.ylabel('Factor de Riesgo')\n"
        "    plt.show()\n"
        "else:\n"
        "    print('Las columnas de factores de riesgo no fueron detectadas con esos nombres específicos.')"
    ),
]
save(os.path.join(NB_DIR, "01_Ideacion_Intento.ipynb"), cells_01)

# ══════════════════════════════════════════════════════════════════
# 02_Suicidio_Gravedad.ipynb
# ══════════════════════════════════════════════════════════════════
cells_02 = [
    md_cell("# 💀 2. Salud: Suicidio (RESULTADO MÁS GRAVE)\n\n👉 Este análisis sirve para validar si los patrones de ideación escalan a hechos consumados de forma proporcional."),
    code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "import os\n\n"
        "sns.set_theme(style='darkgrid')\n"
        "plt.rcParams['figure.figsize'] = (10, 6)"
    ),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "file_path = os.path.join(PROCESSED_DIR, 'p_salud_suicidio.xlsx')\n"
        "df_suicidio = pd.read_excel(file_path)\n"
        "print(f'Total de registros cargados: {len(df_suicidio):,}')\n"
        "display(df_suicidio.head())"
    ),
    md_cell("## 📈 Tendencia\n**¿También está aumentando al igual que la ideación?**"),
    code_cell(
        "col_ano = 'ANO_DEL_HECHO' if 'ANO_DEL_HECHO' in df_suicidio.columns else 'ano'\n"
        "if col_ano in df_suicidio.columns:\n"
        "    tendencia = df_suicidio[col_ano].value_counts().sort_index()\n"
        "    plt.figure(figsize=(10,5))\n"
        "    sns.lineplot(x=tendencia.index, y=tendencia.values, marker='s', color='crimson', linewidth=2)\n"
        "    plt.title('Tendencia Histórica de Suicidios Consumados')\n"
        "    plt.xlabel('Año')\n"
        "    plt.ylabel('Cantidad de Casos')\n"
        "    plt.xticks(tendencia.index)\n"
        "    plt.show()"
    ),
    md_cell("## 📍 Territorial (estandarizado por población)\n**¿Coincide con las mismas localidades de ideación? (Tasa relativa)**"),
    code_cell(
        "col_loc = 'LOCALIDAD_DEL_HECHO' if 'LOCALIDAD_DEL_HECHO' in df_suicidio.columns else 'localidad'\n"
        "if col_loc in df_suicidio.columns:\n"
        "    " + territorial_block("df_suicidio", "col_loc", "mako",
                                   "Tasa de Suicidios Consumados por 100k Habitantes", head=10).replace("\n", "\n    ")
    ),
    md_cell("## 👥 Perfil\n**¿Mismo grupo etario? ¿Mismo sexo predominante?**"),
    code_cell(
        "col_edad = 'GRUPO_DE_EDAD_QUINQUENAL_' if 'GRUPO_DE_EDAD_QUINQUENAL_' in df_suicidio.columns else 'edad'\n"
        "col_sexo = 'SEXO_DE_LA_VICTIMA' if 'SEXO_DE_LA_VICTIMA' in df_suicidio.columns else 'sexo'\n\n"
        "if col_edad in df_suicidio.columns and col_sexo in df_suicidio.columns:\n"
        "    plt.figure(figsize=(12,7))\n"
        "    sns.countplot(data=df_suicidio, y=col_edad, hue=col_sexo,\n"
        "                  order=df_suicidio[col_edad].value_counts().index)\n"
        "    plt.title('Perfil Demográfico: Edad y Sexo en Suicidios')\n"
        "    plt.xlabel('Número de Casos')\n"
        "    plt.ylabel('Grupo de Edad')\n"
        "    plt.legend(title='Sexo')\n"
        "    plt.show()"
    ),
    md_cell("## ⚠️ Causas\n**¿Qué razones o motivos de suicidio aparecen más?**"),
    code_cell(
        "col_razon = 'RAZON_DEL_SUICIDIO' if 'RAZON_DEL_SUICIDIO' in df_suicidio.columns else 'causa'\n"
        "if col_razon in df_suicidio.columns:\n"
        "    razones = df_suicidio[col_razon].value_counts().head(10)\n"
        "    plt.figure(figsize=(12,6))\n"
        "    sns.barplot(x=razones.values, y=razones.index, palette='flare')\n"
        "    plt.title('Principales Razones Reportadas de Suicidio')\n"
        "    plt.xlabel('Frecuencia')\n"
        "    plt.ylabel('Motivo')\n"
        "    plt.show()"
    ),
]
save(os.path.join(NB_DIR, "02_Suicidio_Gravedad.ipynb"), cells_02)

# ══════════════════════════════════════════════════════════════════
# 04_Oferta_Deporte.ipynb
# ══════════════════════════════════════════════════════════════════
cells_04 = [
    md_cell("# 🏃 4. Programas Deporte (OFERTA INSTITUCIONAL)\n\n👉 Representa acceso a bienestar social y prevención de conductas de riesgo."),
    code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "import os\n\n"
        "sns.set_theme(style='darkgrid')\n"
        "plt.rcParams['figure.figsize'] = (10, 6)"
    ),
    md_cell("### Carga y Corrección (Limpieza obligatoria)"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "file_path = os.path.join(PROCESSED_DIR, 'p_programas_deporte.xlsx')\n\n"
        "if os.path.exists(file_path):\n"
        "    df_deporte = pd.read_excel(file_path)\n"
        "    if 'Unnamed: 0' in df_deporte.columns:\n"
        "        print('Corrigiendo encabezados desplazados...')\n"
        "        df_deporte = pd.read_excel(file_path, header=2)\n"
        "    print(f'Total de registros cargados: {len(df_deporte):,}')\n"
        "    display(df_deporte.head(2))\n"
        "    print('\\nColumnas identificadas:', df_deporte.columns.tolist())\n"
        "else:\n"
        "    print('Archivo procesado no encontrado.')"
    ),
    md_cell("## 📍 Cobertura (estandarizada por población)\n**¿En qué localidades hay más programas por habitante?**"),
    code_cell(
        "col_loc = [c for c in df_deporte.columns if 'localidad' in str(c).lower()]\n"
        "if col_loc:\n"
        "    loc_name = col_loc[0]\n"
        "    " + territorial_block("df_deporte", "loc_name", "crest",
                                   "Tasa de Cobertura Deportiva por 100k Habitantes", head=15).replace("\n", "\n    ") + "\n"
        "else:\n"
        "    print('No se detectó columna de localidad en df_deporte.')"
    ),
    md_cell("## 👥 Enfoque e 📊 Intensidad\n**¿Están dirigidos a jóvenes? ¿Cantidad de programas por zona?**"),
    code_cell(
        "print('\\nRevisión estadística rápida de las variables de programa/deporte:')\n"
        "display(df_deporte.describe(include='all'))\n\n"
        "print('\\nNota: Se requiere ahondar en columnas numéricas de asistentes por segmento poblacional.')"
    ),
]
save(os.path.join(NB_DIR, "04_Oferta_Deporte.ipynb"), cells_04)

# ══════════════════════════════════════════════════════════════════
# 05_Oferta_Cultura.ipynb
# ══════════════════════════════════════════════════════════════════
cells_05 = [
    md_cell("# 🎭 5. Centros Culturales (OTRA OFERTA INSTITUCIONAL)\n\n👉 Complementa el deporte (bienestar social) y nos permite ver el mapa de acceso cultural de los jóvenes."),
    code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "import os\n\n"
        "sns.set_theme(style='whitegrid')\n"
        "plt.rcParams['figure.figsize'] = (10, 6)"
    ),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "file_path = os.path.join(PROCESSED_DIR, 'p_centros_culturales_bogota_limpio.xlsx')\n\n"
        "if os.path.exists(file_path):\n"
        "    df_cultura = pd.read_excel(file_path)\n"
        "    print(f'Total de registros cargados: {len(df_cultura):,}')\n"
        "    display(df_cultura.head(3))\n"
        "else:\n"
        "    print('El archivo de Cultura procesado no fue encontrado.')"
    ),
    md_cell("## 📍 Cobertura y densidad (estandarizada por población)\n**¿Cuántos centros culturales existen por cada 100k habitantes por localidad?**"),
    code_cell(
        "if 'localidad' in df_cultura.columns:\n"
        "    " + territorial_block("df_cultura", "'localidad'", "husl",
                                   "Tasa de Centros Culturales por 100k Habitantes", head=20).replace("\n", "\n    ")
    ),
    md_cell("## 🧭 Distribución\n**¿Hay zonas sin acceso? (Lagunas culturales)**"),
    code_cell(
        "if 'localidad' in df_cultura.columns:\n"
        "    baja_cob = df_cultura['localidad'].value_counts()\n"
        "    baja_cob = baja_cob[baja_cob <= 5]\n"
        "    print('⚠️ Zonas con riesgo crítico por baja cobertura cultural (≤5 centros):')\n"
        "    print(baja_cob)\n\n"
        "    if 'upz' in df_cultura.columns:\n"
        "        print(f'\\nTotal de UPZs impactadas culturalmente: {df_cultura[\"upz\"].nunique()} de 117 posibles.')"
    ),
]
save(os.path.join(NB_DIR, "05_Oferta_Cultura.ipynb"), cells_05)

# ══════════════════════════════════════════════════════════════════
# 06_Riesgo_Consumo_SPA.ipynb
# ══════════════════════════════════════════════════════════════════
cells_06 = [
    md_cell("# 💊 6. Salud: Consumo SPA (FACTOR DE RIESGO)\n\n👉 Identifica zonas y poblaciones con mayor riesgo de drogadicción al ser este un co-factor de las ideaciones suicidas."),
    code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "import os\n\n"
        "sns.set_theme(style='whitegrid')\n"
        "plt.rcParams['figure.figsize'] = (10, 6)"
    ),
    md_cell("### Carga de Datos Preprocesados"),
    code_cell(
        "PROCESSED_DIR = '../../01_datos/processed'\n"
        "file_path = os.path.join(PROCESSED_DIR, 'p_salud_consumo.xlsx')\n\n"
        "if os.path.exists(file_path):\n"
        "    df_spa = pd.read_excel(file_path)\n"
        "    print(f'Total de registros cargados: {len(df_spa):,}')\n"
        "    display(df_spa.head(3))\n"
        "else:\n"
        "    print('El archivo de Consumo SPA procesado no fue encontrado.')"
    ),
    md_cell("## 📈 Tendencia\n**¿Aumenta el consumo históricamente?**"),
    code_cell(
        "if 'ANO' in df_spa.columns:\n"
        "    tendencia = df_spa['ANO'].value_counts().sort_index()\n"
        "    plt.figure(figsize=(10,5))\n"
        "    sns.lineplot(x=tendencia.index, y=tendencia.values, marker='D', color='purple', linewidth=2)\n"
        "    plt.title('Curva Histórica de Casos de Consumo SPA')\n"
        "    plt.xlabel('Año')\n"
        "    plt.ylabel('Cantidad de Requerimientos')\n"
        "    plt.xticks(tendencia.index)\n"
        "    plt.show()"
    ),
    md_cell("## 📍 Territorial (estandarizado por población)\n**¿Dónde es más alta la tasa de consumo por habitante?**"),
    code_cell(
        "col_loc_spa = 'NOMBRELOCALIDADRESIDENCIA' if 'NOMBRELOCALIDADRESIDENCIA' in df_spa.columns else None\n"
        "if col_loc_spa:\n"
        "    " + territorial_block("df_spa", "col_loc_spa", "inferno",
                                   "Tasa de Consumo SPA por 100k Habitantes", head=10).replace("\n", "\n    ") + "\n"
        "else:\n"
        "    print('No se encontró columna de localidad en df_spa.')"
    ),
    md_cell("## 📌 Contexto\n**¿Dónde consumen (parques, vivienda, vía pública)?**"),
    code_cell(
        "cols_contexto = [col for col in df_spa.columns if 'SITIO' in col]\n"
        "if cols_contexto:\n"
        "    df_contexto = df_spa[cols_contexto].copy()\n"
        "    for c in cols_contexto:\n"
        "        df_contexto[c] = pd.to_numeric(df_contexto[c], errors='coerce').fillna(0)\n"
        "    sumas_contexto = df_contexto.sum().sort_values(ascending=False)\n"
        "    plt.figure(figsize=(12,6))\n"
        "    sns.barplot(x=sumas_contexto.values, y=sumas_contexto.index, palette='YlOrBr_r')\n"
        "    plt.title('Sitio Habitual de Consumo más recurrente')\n"
        "    plt.xlabel('Veces Mencionado')\n"
        "    plt.show()"
    ),
    md_cell("## 👥 Perfil\n**Edad / ciclo de vida y Sexo predominante**"),
    code_cell(
        "if 'CURSO_DE_VIDA' in df_spa.columns and 'SEXO' in df_spa.columns:\n"
        "    plt.figure(figsize=(12,7))\n"
        "    sns.countplot(data=df_spa, y='CURSO_DE_VIDA', hue='SEXO', palette='pastel',\n"
        "                  order=df_spa['CURSO_DE_VIDA'].value_counts().index)\n"
        "    plt.title('Distribución de Consumidores por Curso de Vida y Sexo')\n"
        "    plt.xlabel('Volumen de Casos')\n"
        "    plt.ylabel('Curso de Vida')\n"
        "    plt.show()"
    ),
]
save(os.path.join(NB_DIR, "06_Riesgo_Consumo_SPA.ipynb"), cells_06)

print("\n✅ Todos los notebooks han sido reconstruidos correctamente.")
