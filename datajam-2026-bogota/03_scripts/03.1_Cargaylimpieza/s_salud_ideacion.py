# [FASE 2] Carga y Limpieza: Salud Mental - Ideacion

import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# 1. Carga de los Datos
ruta_crudos = '../01_datos/raw/r_salud_ideacion.xlsx'
print(f"Cargando Ideacion e Intento desde {ruta_crudos} ...")

df_raw = pd.read_excel(ruta_crudos, engine='openpyxl')
filas_orig, col_orig = df_raw.shape
print(f"Dimensiones iniciales: {filas_orig} filas, {col_orig} columnas.")

# 2. Limpieza de Vacios (NaN)
df_clean = df_raw.dropna(axis=1, how='all')
df_clean = df_clean.dropna(axis=0, how='all')

filas_fin, col_fin = df_clean.shape
print(f"Dimensiones tras filtrado: {filas_fin} filas.")

# 3. Exportacion (Unicamente XLSX)
ruta_excel = '../01_datos/processed/p_salud_ideacion.xlsx'

df_clean.to_excel(ruta_excel, index=False)
print("Archivo de Excel limpio exportado exitosamente.")

# 4. Reporte de Limpieza de Datos
print("="*40)
print("\U0001f4c4 REPORTE DE LIMPIEZA - IDEACION")
print("="*40)
print(f"Filas originales: {filas_orig}")
print(f"Filas tras la limpieza: {filas_fin}")
print(f"Total de registros eliminados: {filas_orig - filas_fin}")
if filas_orig > 0:
    print(f"Porcentaje de retencion: {round((filas_fin/filas_orig)*100, 2)}%")
print("="*40)


