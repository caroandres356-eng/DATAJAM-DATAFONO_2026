"""
convert_to_parquet.py
Convierte los archivos xlsx lentos a parquet para carga instantánea en los notebooks.
También detecta el header correcto del archivo de deporte.
"""
import pandas as pd
import os
import time

PROCESSED_DIR = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\01_datos\processed"

conversiones = {
    'p_salud_suicidio.xlsx':                    'p_salud_suicidio.parquet',
    'p_condiciones_habitabilidad.xlsx':          'p_condiciones_habitabilidad.parquet',
    'p_centros_culturales_bogota_limpio.xlsx':   'p_centros_culturales_bogota_limpio.parquet',
    'p_salud_ideacion.xlsx':                     'p_salud_ideacion.parquet',
    'p_salud_consumo.xlsx':                      'p_salud_consumo.parquet',
}

for xlsx_name, parquet_name in conversiones.items():
    xlsx_path    = os.path.join(PROCESSED_DIR, xlsx_name)
    parquet_path = os.path.join(PROCESSED_DIR, parquet_name)
    if os.path.exists(parquet_path):
        print(f"  [skip] {parquet_name} ya existe")
        continue
    print(f"  Convirtiendo {xlsx_name} ...", end=" ", flush=True)
    t0 = time.time()
    df = pd.read_excel(xlsx_path)
    # Normalizar nombres de columnas: minúsculas sin espacios
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    df.to_parquet(parquet_path, index=False)
    print(f"{len(df):,} filas | {time.time()-t0:.1f}s")

# Deporte tiene header en fila 2
deporte_xlsx    = os.path.join(PROCESSED_DIR, 'p_programas_deporte.xlsx')
deporte_parquet = os.path.join(PROCESSED_DIR, 'p_programas_deporte.parquet')
if not os.path.exists(deporte_parquet):
    print(f"  Convirtiendo p_programas_deporte.xlsx (header=2) ...", end=" ", flush=True)
    t0 = time.time()
    df = pd.read_excel(deporte_xlsx, header=2)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    df.to_parquet(deporte_parquet, index=False)
    print(f"{len(df):,} filas | {time.time()-t0:.1f}s")
else:
    print("  [skip] p_programas_deporte.parquet ya existe")

print("\nColumnas relevantes por archivo:")
for pq in ['p_salud_suicidio.parquet', 'p_condiciones_habitabilidad.parquet',
           'p_programas_deporte.parquet', 'p_centros_culturales_bogota_limpio.parquet',
           'p_salud_consumo.parquet']:
    path = os.path.join(PROCESSED_DIR, pq)
    if os.path.exists(path):
        df_tmp = pd.read_parquet(path)
        loc_cols = [c for c in df_tmp.columns if 'local' in c.lower()]
        print(f"  {pq}: localidad={loc_cols} | total_cols={len(df_tmp.columns)}")

print("\nDone.")
