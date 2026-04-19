import pandas as pd

archivos = {
    'centros_culturales': '../01_datos/processed/p_centros_culturales_bogota_limpio.xlsx',
    'habitabilidad': '../01_datos/processed/p_condiciones_habitabilidad.xlsx',
    'deporte': '../01_datos/processed/p_programas_deporte.xlsx',
    'consumo': '../01_datos/processed/p_salud_consumo.xlsx',
    'ideacion': '../01_datos/processed/p_salud_ideacion.xlsx',
    'suicidio': '../01_datos/processed/p_salud_suicidio.xlsx',
}

for nombre, ruta in archivos.items():
    df = pd.read_excel(ruta, nrows=2)
    print(f'=== {nombre} ({df.shape[1]} cols) ===')
    print(list(df.columns))
    print()
