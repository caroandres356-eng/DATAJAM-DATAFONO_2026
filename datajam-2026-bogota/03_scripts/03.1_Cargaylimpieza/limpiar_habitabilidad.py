import pandas as pd
import numpy as np
import warnings
import os

warnings.filterwarnings('ignore')

def limpiar_datos():
    # Rutas
    base_dir = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota"
    ruta_crudos = os.path.join(base_dir, '01_datos', 'raw', 'r_condiciones_habitabilidad_accesibilidad_2024.xlsx')
    ruta_excel = os.path.join(base_dir, '01_datos', 'processed', 'p_condiciones_habitabilidad.xlsx')

    print(f"Cargando Condiciones de Habitabilidad desde {ruta_crudos} ...")
    
    df_raw = pd.read_excel(ruta_crudos, engine='openpyxl')
    filas_orig, col_orig = df_raw.shape
    print(f"Dimensiones iniciales: {filas_orig} filas, {col_orig} columnas.")
    
    # 2. Limpieza de Vacíos
    # Eliminamos columnas/filas totalmente vacías
    df_clean = df_raw.dropna(axis=1, how='all')
    df_clean = df_clean.dropna(axis=0, how='all')
    
    # Exigimos registro espacial: localidad y UPZ son cruciales para el cluster
    df_clean = df_clean.dropna(subset=['localidad', 'loccodigo', 'upzcodigo'])

    filas_fin, col_fin = df_clean.shape
    print(f"Dimensiones tras filtrado espacial: {filas_fin} filas.")
    
    # 3. Exportación
    print(f"Guardando archivo limpio en: {ruta_excel}")
    df_clean.to_excel(ruta_excel, index=False)
    print("Archivo de Excel limpio exportado exitosamente.")
    
    # 4. Reporte
    print("="*40)
    print("📄 REPORTE DE LIMPIEZA - HABITABILIDAD")
    print("="*40)
    print(f"Filas originales: {filas_orig}")
    print(f"Filas tras la limpieza: {filas_fin}")
    print(f"Total de registros eliminados: {filas_orig - filas_fin}")
    if filas_orig > 0:
        print(f"Porcentaje de retención: {round((filas_fin/filas_orig)*100, 2)}%")
    print("="*40)

if __name__ == "__main__":
    limpiar_datos()
