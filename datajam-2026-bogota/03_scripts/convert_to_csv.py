"""
convert_to_csv.py
Convierte los archivos xlsx a CSV para carga rápida en los notebooks.
Detecta el header correcto del archivo de deporte (header=2).
"""
import pandas as pd
import os
import time

PROCESSED_DIR = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\01_datos\processed"

conversiones = {
    'p_salud_suicidio.xlsx':                    ('p_salud_suicidio.csv',                   0),
    'p_condiciones_habitabilidad.xlsx':          ('p_condiciones_habitabilidad.csv',         0),
    'p_centros_culturales_bogota_limpio.xlsx':   ('p_centros_culturales_bogota_limpio.csv',  0),
    'p_salud_ideacion.xlsx':                     ('p_salud_ideacion.csv',                    0),
    'p_salud_consumo.xlsx':                      ('p_salud_consumo.csv',                     0),
    'p_programas_deporte.xlsx':                  ('p_programas_deporte.csv',                 2),
}

for xlsx_name, (csv_name, header_row) in conversiones.items():
    xlsx_path = os.path.join(PROCESSED_DIR, xlsx_name)
    csv_path  = os.path.join(PROCESSED_DIR, csv_name)

    if os.path.exists(csv_path):
        print(f"  [skip] {csv_name} ya existe")
        continue

    print(f"  Convirtiendo {xlsx_name} ...", end=" ", flush=True)
    t0 = time.time()
    df = pd.read_excel(xlsx_path, header=header_row)
    # Normalizar columnas: strip + lower + reemplazar espacios por _
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    elapsed = time.time() - t0
    print(f"{len(df):,} filas | {elapsed:.1f}s -> {csv_name}")

print("\n--- Columnas de localidad detectadas ---")
for csv_name in ['p_salud_suicidio.csv', 'p_condiciones_habitabilidad.csv',
                 'p_programas_deporte.csv', 'p_centros_culturales_bogota_limpio.csv',
                 'p_salud_consumo.csv']:
    path = os.path.join(PROCESSED_DIR, csv_name)
    if os.path.exists(path):
        df_tmp = pd.read_csv(path, nrows=2, encoding='utf-8-sig')
        loc_cols = [c for c in df_tmp.columns if 'local' in c.lower()]
        print(f"  {csv_name}: localidad_cols={loc_cols}")

print("\nConversion completa.")
