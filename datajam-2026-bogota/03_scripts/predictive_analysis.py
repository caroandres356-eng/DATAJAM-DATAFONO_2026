import os
import argparse
import json
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', '01_datos', 'processed')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '05_outputs', 'predicciones')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_localidad_series(series):
    return (
        series.astype(str).str.lower().str.strip()
        .str.normalize('NFKD')
        .str.encode('ascii', errors='ignore').str.decode('utf-8')
        .str.replace(r'^\d+\s*-\s*', '', regex=True)
    )


def build_master(localidad_filter=None):
    # Load inputs (expect processed CSVs to exist)
    df_pob = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_poblacion_bogota.csv'))
    df_pob['localidad_clean'] = clean_localidad_series(df_pob['localidad'])

    df_suicidio = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_salud_suicidio.csv'),
                              usecols=['localidad_del_hecho', 'ano_del_hecho', 'ciclo_vital'])
    df_suicidio['localidad_clean'] = clean_localidad_series(df_suicidio['localidad_del_hecho'])
    df_suicidio['anio'] = pd.to_numeric(df_suicidio['ano_del_hecho'], errors='coerce')

    df_ideacion = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_salud_ideacion.csv'),
                              usecols=['localidad_residencia', 'ano_notificacion', 'ciclovital'])
    df_ideacion['localidad_clean'] = clean_localidad_series(df_ideacion['localidad_residencia'])
    df_ideacion['anio'] = pd.to_numeric(df_ideacion['ano_notificacion'], errors='coerce')

    df_spa = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_salud_consumo.csv'),
                         usecols=['nombrelocalidadresidencia', 'ano', 'curso_de_vida'])
    df_spa['localidad_clean'] = clean_localidad_series(df_spa['nombrelocalidadresidencia'])
    df_spa['anio'] = pd.to_numeric(df_spa['ano'], errors='coerce')

    df_deporte = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_programas_deporte.csv'), usecols=['localidad'])
    df_deporte['localidad_clean'] = clean_localidad_series(df_deporte['localidad'])

    df_cultura = pd.read_csv(os.path.join(PROCESSED_DIR, 'p_centros_culturales_bogota_limpio.csv'), usecols=['localidad'])
    df_cultura['localidad_clean'] = clean_localidad_series(df_cultura['localidad'])

    agg_s = df_suicidio.groupby(['localidad_clean', 'anio']).size().reset_index(name='suicidios')
    agg_i = df_ideacion.groupby(['localidad_clean', 'anio']).size().reset_index(name='ideaciones')
    agg_spa = df_spa.groupby(['localidad_clean', 'anio']).size().reset_index(name='spa')

    df_master = agg_s.merge(agg_i, on=['localidad_clean', 'anio'], how='outer')\
                     .merge(agg_spa, on=['localidad_clean', 'anio'], how='outer').fillna(0)

    df_off = df_deporte.groupby('localidad_clean').size().reset_index(name='oferta_deporte')\
                   .merge(df_cultura.groupby('localidad_clean').size().reset_index(name='oferta_cultura'),
                          on='localidad_clean', how='outer').fillna(0)

    df_final = df_master.merge(df_pob[['localidad_clean', 'localidad', 'poblacion']], on='localidad_clean', how='left')
    df_final = df_final.merge(df_off, on='localidad_clean', how='left').fillna(0)

    df_final = df_final[(df_final['poblacion'] > 50000) & (df_final['localidad_clean'] != 'sumapaz')]

    for c in ['suicidios', 'ideaciones', 'spa', 'oferta_deporte', 'oferta_cultura']:
        df_final[f'tasa_{c}'] = (df_final[c] / df_final['poblacion']) * 100000

    if localidad_filter:
        df_final = df_final[df_final['localidad'].str.lower() == localidad_filter.lower()]

    return df_final


def run_prediction(localidad='Ciudad Bolivar', forecast_steps=12):
    df_final = build_master(localidad_filter=None)
    # identify loc_prioritaria if not provided
    risk_res = df_final.groupby('localidad')[['tasa_suicidios', 'tasa_ideaciones', 'tasa_spa']].mean()
    risk_res_normalized = (risk_res - risk_res.min()) / (risk_res.max() - risk_res.min()).replace(0, 1)
    risk_res['indice_riesgo'] = risk_res_normalized.mean(axis=1)
    off_res = df_final.groupby('localidad')[['tasa_oferta_deporte', 'tasa_oferta_cultura']].mean()
    off_res_normalized = (off_res - off_res.min()) / (off_res.max() - off_res.min()).replace(0, 1)
    off_res['indice_oferta'] = off_res_normalized.mean(axis=1)
    df_gap = risk_res[['indice_riesgo']].join(off_res[['indice_oferta']])
    df_gap['brecha_abandono'] = df_gap['indice_riesgo'] - df_gap['indice_oferta']

    if localidad is None:
        localidad = df_gap.sort_values('brecha_abandono', ascending=False).index[0]

    localidad = localidad.title()
    df_pred = df_final[df_final['localidad'] == localidad].sort_values('anio').copy()
    if df_pred.empty:
        raise ValueError(f'No hay datos para la localidad {localidad}')

    serie_riesgo = df_pred.set_index('anio')['tasa_suicidios'].astype(float).dropna()

    # ARIMA (annual data)
    arima_result = None
    try:
        model_arima = SARIMAX(serie_riesgo, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0),
                              enforce_stationarity=False, enforce_invertibility=False)
        results_arima = model_arima.fit(disp=False)
        arima_forecast = results_arima.get_forecast(steps=forecast_steps)
        arima_ci = arima_forecast.conf_int(alpha=0.05)
        arima_df = pd.DataFrame({
            'year': [int(serie_riesgo.index.max() + i) for i in range(1, forecast_steps+1)],
            'pred_arima': arima_forecast.predicted_mean.values,
            'low_arima': arima_ci.iloc[:, 0].values,
            'high_arima': arima_ci.iloc[:, 1].values,
        })
        arima_result = {'aic': results_arima.aic, 'bic': results_arima.bic}
    except Exception as e:
        arima_df = pd.DataFrame()
        arima_result = {'error': str(e)}

    # Exponential Smoothing
    try:
        model_es = ExponentialSmoothing(serie_riesgo, trend='add', seasonal=None, initialization_method='estimated')
        results_es = model_es.fit()
        es_forecast = results_es.forecast(steps=forecast_steps)
        es_df = pd.DataFrame({
            'year': [int(serie_riesgo.index.max() + i) for i in range(1, forecast_steps+1)],
            'pred_es': es_forecast.values,
        })
        es_result = {'aic': results_es.aic, 'ssr': results_es.ssr}
    except Exception as e:
        es_df = pd.DataFrame()
        es_result = {'error': str(e)}

    # Merge predictions
    if not arima_df.empty and not es_df.empty:
        forecast = arima_df.merge(es_df, on='year', how='outer')
    elif not arima_df.empty:
        forecast = arima_df
    else:
        forecast = es_df

    out_csv = os.path.join(OUTPUT_DIR, f'forecast_{localidad.lower().replace(" ", "_")}.csv')
    forecast.to_csv(out_csv, index=False)

    meta = {
        'localidad': localidad,
        'historical_years': int(len(serie_riesgo)),
        'last_year': int(serie_riesgo.index.max()),
        'arima': arima_result,
        'es': es_result,
        'forecast_file': out_csv,
    }
    meta_file = out_csv.replace('.csv', '_meta.json')
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f'✅ Predicción completada para {localidad}. Archivos:')
    print(' -', out_csv)
    print(' -', meta_file)

    return forecast, meta


def main():
    parser = argparse.ArgumentParser(description='Predictive analysis for locality')
    parser.add_argument('--localidad', type=str, default='Ciudad Bolivar')
    parser.add_argument('--steps', type=int, default=12)
    args = parser.parse_args()

    run_prediction(localidad=args.localidad, forecast_steps=args.steps)


if __name__ == '__main__':
    main()
