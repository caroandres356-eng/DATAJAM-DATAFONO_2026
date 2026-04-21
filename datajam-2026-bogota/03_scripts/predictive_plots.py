import os
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '05_outputs', 'predicciones')
PLOTS_DIR = os.path.join(os.path.dirname(__file__), '..', '05_outputs', 'graficos_predictivos')
os.makedirs(PLOTS_DIR, exist_ok=True)


def make_plots(localidad='Ciudad Bolivar'):
    fpath = os.path.join(OUTPUT_DIR, f'forecast_{localidad.lower().replace(" ", "_")}.csv')
    if not os.path.exists(fpath):
        raise FileNotFoundError(f'Forecast file not found: {fpath}')

    df_fore = pd.read_csv(fpath)

    # try load historical series from processed (if available)
    processed_hist = os.path.join(os.path.dirname(__file__), '..', '01_datos', 'processed', 'p_poblacion_bogota.csv')

    # Plot predictions
    plt.figure(figsize=(12, 6))
    years = df_fore['year']
    if 'pred_arima' in df_fore.columns:
        plt.plot(years, df_fore['pred_arima'], label='ARIMA', marker='s')
        plt.fill_between(years, df_fore.get('low_arima', df_fore['pred_arima']), df_fore.get('high_arima', df_fore['pred_arima']), alpha=0.2)
    if 'pred_es' in df_fore.columns:
        plt.plot(years, df_fore['pred_es'], label='ExpSmooth', marker='^')

    plt.title(f'Predicciones de Tasa de Suicidios para {localidad}')
    plt.xlabel('Año')
    plt.ylabel('Tasa por 100k habitantes')
    plt.legend()
    plt.grid(True, alpha=0.3)

    out_png = os.path.join(PLOTS_DIR, f'forecast_{localidad.lower().replace(" ", "_")}.png')
    plt.savefig(out_png, dpi=200, bbox_inches='tight')
    plt.close()

    # Save backing CSV used for plots
    out_backing = os.path.join(PLOTS_DIR, f'backing_data_{localidad.lower().replace(" ", "_")}.csv')
    df_fore.to_csv(out_backing, index=False)

    print('✅ Gráficos y datos de respaldo guardados:')
    print(' -', out_png)
    print(' -', out_backing)


if __name__ == '__main__':
    make_plots()
