# [FASE 2] Carga y Limpieza: Centros Culturales Bogotá

import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# 1. Carga de los Datos
ruta_crudos = '../01_datos/raw/r_centros_culturales.csv'
print(f"Cargando Centros Culturales desde {ruta_crudos} ...")

df_raw = pd.read_csv(ruta_crudos, encoding='latin-1', sep=';', on_bad_lines='skip')
filas_orig, col_orig = df_raw.shape
print(f"Dimensiones iniciales: {filas_orig} filas, {col_orig} columnas.")

# 2. Filtrado de Columnas Utiles
columnas_clave = [
    'nombre_del_museo',
    'direccion',
    'localidad',
    'upz',
    'nombre_de_la_entidad_administradora_del_equipamiento',
    'caracter',
    'uso_principal'
]
columnas_presentes = [col for col in columnas_clave if col in df_raw.columns]
df_clean = df_raw[columnas_presentes].copy()

# 3. Limpieza de Vacios y Nomenclatura
df_clean = df_clean.dropna(axis=0, how='all')
df_clean.replace('N.D', pd.NA, inplace=True)

# Exigimos registro espacial: localidad es crucial para el cruce
df_clean = df_clean.dropna(subset=['localidad'])

# Estandarizar texto
for col in df_clean.select_dtypes(include='object').columns:
    df_clean[col] = df_clean[col].str.strip()

df_clean['uso_principal'] = 'Centro Cultural y Artístico'

# Renombrar columnas
df_clean.rename(columns={
    'nombre_del_museo': 'nombre',
    'direccion': 'direccion',
    'localidad': 'localidad',
    'upz': 'upz',
    'nombre_de_la_entidad_administradora_del_equipamiento': 'entidad_administradora',
    'caracter': 'caracter',
    'uso_principal': 'uso_principal'
}, inplace=True)

filas_fin, col_fin = df_clean.shape
print(f"Dimensiones tras filtrado: {filas_fin} filas.")

# 4. Exportacion (Unicamente XLSX)
ruta_excel = '../01_datos/processed/p_centros_culturales.xlsx'

df_clean.to_excel(ruta_excel, index=False)
print("Archivo de Excel limpio exportado exitosamente.")

# 5. Reporte de Limpieza de Datos
print("="*40)
print("\U0001f4c4 REPORTE DE LIMPIEZA - CENTROS CULTURALES")
print("="*40)
print(f"Filas originales: {filas_orig}")
print(f"Filas tras la limpieza: {filas_fin}")
print(f"Total de registros eliminados: {filas_orig - filas_fin}")
if filas_orig > 0:
    print(f"Porcentaje de retencion: {round((filas_fin/filas_orig)*100, 2)}%")
print("="*40)
