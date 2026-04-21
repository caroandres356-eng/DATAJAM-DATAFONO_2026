import pandas as pd
import time
import os

PROCESSED_DIR = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\01_datos\processed"

files = {
    'suicidio':     'p_salud_suicidio.xlsx',
    'habitabilidad':'p_condiciones_habitabilidad.xlsx',
    'deporte':      'p_programas_deporte.xlsx',
    'cultura':      'p_centros_culturales_bogota_limpio.xlsx',
}
for name, fname in files.items():
    path = os.path.join(PROCESSED_DIR, fname)
    t0 = time.time()
    df = pd.read_excel(path)
    t1 = time.time()
    print(f"[{name}] {len(df):,} filas | {t1-t0:.1f}s | cols: {df.columns.tolist()}")

# Detectar header correcto en deporte
print("\n--- Detectando header correcto en deporte ---")
path_dep = os.path.join(PROCESSED_DIR, 'p_programas_deporte.xlsx')
for h in [0, 1, 2, 3]:
    df2 = pd.read_excel(path_dep, header=h)
    cols_lower = [str(c).lower() for c in df2.columns]
    if any('local' in c for c in cols_lower):
        loc_cols = [c for c in df2.columns if 'local' in str(c).lower()]
        print(f"  header={h} -> columnas con 'local': {loc_cols}")
    else:
        print(f"  header={h} -> {df2.columns.tolist()[:6]}")
