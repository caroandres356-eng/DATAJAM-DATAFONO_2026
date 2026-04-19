<<<<<<<<< Temporary merge branch 1
# DATAJAM-DATAFONO_2026
=========
# DataJam Datáfono 2026 - Bogotá

Este repositorio contiene la estructura base para el proyecto desarrollado durante la DataJam 2026, enfocado en Bogotá. 

## Fases de Desarrollo del Proyecto

El ciclo de vida del proyecto sigue un flujo estructurado de preparación, análisis y entrega de resultados:

```text
  FASE 1: SELECCIÓN          FASE 2: PREPARACIÓN            FASE 3: ANÁLISIS
 ╭──────────────────╮       ╭──────────────────╮           ╭──────────────────╮
 │ Fuentes de       │       │ Python (limpia)  │           │ Python (EDA)     │
 │ Datos Públicos   │──────▶│ pandas / NumPy   │──────────▶│ clustering       │
 │ de Bogotá        │       │                  │           │ correlaciones    │
 ╰──────────────────╯       ╰──────────────────╯           ╰────────┬─────────╯
                                                                    │
                                            FASE 4: VISUALIZACIÓN ◀─╯
                                           ╭──────────────────╮
                                           │ Power BI         │
                                           │ Dashboards       │
                                           │ Interactivos     │
                                           ╰────────┬─────────╯
                                                    │
                               ╭────────────────────┴────────────────────╮
                               ▼                                         ▼
  FASE 5: PROFUNDIZACIÓN                            FASE 6: CONCLUSIONES
 ╭──────────────────╮                              ╭──────────────────╮
 │ TimesFM          │                              │ Storytelling     │
 │ (OPCIONAL)       │                              │ + Recomenda-     │
 │ Predicciones     │                              │   ciones         │
 ╰──────────────────╯                              ╰──────────────────╯
```

## Estructura de Carpetas

A continuación se detalla cómo las fases del proyecto se mapean dentro del directorio y dónde ubicar cada componente, integrando la predicción mediante **TimesFM**:

```text
datajam-2026-bogota/
│
├── 01_datos/
│   ├── raw/                           # [FASE 1] Datos sin modificar (movilidad.csv, seguridad.csv).
│   ├── processed/                     # [FASE 2] Datos limpios post-ETL listos para análisis.
│   └── external/                      # [FASE 1] Datos complementarios (ej. geometrías, geojson).
│
├── 02_notebooks/                      # [FASE 2, 3 y 5] Notebooks interactivos (.ipynb).
│   │                                  # - Exploración y EDA.
│   │                                  # - Clustering iterativo.
│   │                                  # - Implementación y pruebas de TimesFM.
│   └── 04_timesfm_prediccion.ipynb    # <--- Experimentación y configuración del modelo predictivo.
│
├── 03_scripts/                        # Scripts de automatización y producción (.py).
│   │                                  # Funciones de limpieza y modelos modulares.
│   └── forecasting_timesfm.py         # <--- (Opcional) Script automatizado para correr la predicción.
│
├── 04_powerbi/                        # [FASE 4] Reportes y visualizaciones.
│   │                                  # Archivo principal .pbix.
│   └── capturas/                      # Screenshots previas del dashboard listos.
│
├── 05_outputs/
│   ├── graficos/                      # [FASE 3] Gráficos exportados (codo, dispersión, etc).
│   ├── tablas/                        # [FASE 3] Resúmenes numéricos y perfiles de clusters.
│   └── predicciones/                  # [FASE 5] Output de TimesFM 
│       └── forecast_2026.csv          # <--- Archivo exportado con proyecciones futuras (series de tiempo).
│
├── 06_presentacion/                   # [FASE 6] Cierre y comunicación de resultados.
│   │                                  # Documento base para el pitch y storytelling.
│   └── imagenes/                      # Material de apoyo extra (logos, iconos) para diapositivas.
```
