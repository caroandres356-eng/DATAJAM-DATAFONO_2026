# [FASE 2] Carga y Limpieza: Hogares Economico

import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# 1. Carga de los Datos
ruta_crudos = '../01_datos/raw/r_hogares_economico.xlsx'
print(f"Cargando Hogares desde {ruta_crudos} ...")

df_raw = pd.read_excel(ruta_crudos, engine='openpyxl')
filas_orig, col_orig = df_raw.shape
print(f"Dimensiones iniciales: {filas_orig} filas, {col_orig} columnas.")

# 2. Filtrado de Columnas Utiles
columnas_clave = [
    'N_ingpc', 'N_pobre_monetario', 'N_pobre_extremo', 'N_pobre_ipm',
    'N_estrato',
    'N_pisos', 'N_paredes', 'N_hacinamiento', 'N_agua', 'N_alcantarillado', 'N_energia',
    'N_ocupados', 'N_informal', 'N_bajo_logro',
    'N_codigo_localidad_trabajo'
]

columnas_presentes = [col for col in columnas_clave if col in df_raw.columns]
df_clean = df_raw[columnas_presentes].copy()

# Quitamos registros cuya localidad sea vacia
if 'N_codigo_localidad_trabajo' in df_clean.columns:
    df_clean = df_clean.dropna(subset=['N_codigo_localidad_trabajo'])

filas_fin, col_fin = df_clean.shape
print(f"Dimensiones tras filtrado: {filas_fin} filas.")

# 3. Exportacion (Unicamente XLSX)
ruta_excel = '../01_datos/processed/p_hogares_economico.xlsx'

df_clean.to_excel(ruta_excel, index=False)
print("Archivo de Excel limpio exportado exitosamente.")

# 4. Reporte de Limpieza de Datos
print("="*40)
print("\U0001f4c4 REPORTE DE LIMPIEZA DE DATOS - HOGARES")
print("="*40)
print(f"Filas originales: {filas_orig}")
print(f"Filas tras la limpieza: {filas_fin}")
print(f"Total de registros eliminados: {filas_orig - filas_fin}")
if filas_orig > 0:
    print(f"Porcentaje de retencion: {round((filas_fin/filas_orig)*100, 2)}%")
print("="*40)


