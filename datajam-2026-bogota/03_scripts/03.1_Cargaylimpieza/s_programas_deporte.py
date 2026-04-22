# [FASE 2] Carga y Limpieza: Programas Deporte - VERSIÓN CORREGIDA

import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# 1. Carga de los Datos - saltando las filas de encabezado malas
ruta_crudos = '../01_datos/raw/r_programas_deporte.xlsx'
print(f"Cargando Programas desde {ruta_crudos} ...")

# CORRECCIÓN PRINCIPAL: skiprows=2 para saltar:
# - Fila 0: "ACTIVIDADES PROGRAMAS BOGOTA EN FORMA _I SEMESTRE 2025"
# - Fila 1: (si hay otra fila de metadata)
df_raw = pd.read_excel(ruta_crudos, engine='openpyxl', skiprows=1)

filas_orig, col_orig = df_raw.shape
print(f"Dimensiones iniciales: {filas_orig} filas, {col_orig} columnas.")
print(f"Columnas detectadas: {df_raw.columns.tolist()}")

# 2. Limpieza de Vacios y Nomenclatura
df_clean = df_raw.dropna(axis=0, how='all')

# CORRECCIÓN: Limpiar nombres de columnas pero mantener los originales si son válidos
df_clean.columns = [str(c).strip().lower().replace(' ', '_').replace('#', 'num') for c in df_clean.columns]

# Eliminar filas donde 'mes' esté vacío (son filas de totales o notas)
df_clean = df_clean[df_clean['mes'].notna()]
df_clean = df_clean[df_clean['mes'] != '']

filas_fin, col_fin = df_clean.shape
print(f"Dimensiones relevantes: {filas_fin} filas.")

# 3. Exportacion (Unicamente XLSX)
ruta_excel = '../01_datos/processed/p_programas_deporte.xlsx'

df_clean.to_excel(ruta_excel, index=False)
print("✅ Archivo de Excel limpio exportado exitosamente.")

# 4. Reporte de Limpieza de Datos
print("="*50)
print("📋 REPORTE DE LIMPIEZA - PROGRAMAS DE DEPORTE")
print("="*50)
print(f"Filas originales (con encabezados): {filas_orig}")
print(f"Filas tras la limpieza: {filas_fin}")
print(f"Total de registros eliminados: {filas_orig - filas_fin}")
if filas_orig > 0:
    print(f"Porcentaje de retencion: {round((filas_fin/filas_orig)*100, 2)}%")
print("="*50)
print("📊 Vista previa de datos limpios:")
print(df_clean.head())
print("="*50)