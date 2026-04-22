# 📑 Nota Técnica: Integración de Datos y Desafíos Técnicos
**Proyecto: Riesgo Suicida vs Oferta Institucional - Bogotá DataJam 2026**

## 1. Dificultades en el Acceso y Calidad de Datos
Durante la fase inicial del proyecto, se identificaron varios retos relacionados con la heterogeneidad de los formatos disponibles en el portal de **Datos Abiertos Bogotá**:
- **Formatos Inconsistentes**: Los archivos originales se encontraban mayoritariamente en formato Excel (`.xlsx`), lo cual generaba cuellos de botella en la lectura automatizada debido al tamaño de las hojas. Se optó por una fase de pre-procesamiento para convertir todos los insumos críticos a formato CSV.
- **Nombres de Localidades**: Se detectó una alta variabilidad en el registro de nombres (ej: "Santa Fe" vs "Santafe", "Usaquén" vs "Usaquen", o prefijos numéricos como "01 - Usaquén"). Esto requirió el desarrollo de una función de estandarización basada en normalización Unicode y expresiones regulares.

## 2. Retos en la Integración de Fuentes
La consolidación del dataset maestro territorial enfrentó los siguientes desafíos:
- **Diferencia de Granularidad**: Mientras los datos de salud (suicidio e ideación) tenían registros individuales por fecha, los datos de oferta institucional estaban agregados por sede o programa. Se implementó una lógica de agregación anual por localidad para permitir el cruce estadístico.
- **Normalización Poblacional**: Para comparar equitativamente localidades con densidades dispares (ej: Suba vs Candelaria), fue imperativo integrar las proyecciones poblacionales y calcular tasas por cada 100,000 habitantes, evitando el sesgo de "números absolutos".

## 3. Limitaciones Encontradas
- **Ventana Temporal**: No todos los datasets cubrían el mismo rango histórico (algunos iniciaban en 2012 y otros en 2015). El análisis de correlación se limitó a los años con intersección de datos completa (2019-2023).
- **Subregistro**: Como en todo estudio de salud mental, los datos dependen de la notificación oficial, lo que podría implicar un subregistro en zonas de difícil acceso institucional.

## 4. Recomendaciones para el Uso de Datos Públicos
- **Adopción de Formatos Abiertos**: Se sugiere a las entidades distritales priorizar la publicación en formatos planos (CSV/Parquet) sobre archivos Excel multihidra para facilitar el análisis masivo.
- **Diccionarios de Datos Unificados**: La estandarización de los nombres de las 20 localidades debería ser un estándar transversal en todos los datasets del distrito para reducir el tiempo de limpieza en proyectos de analítica integrada.

---
**Elaborado para:** Bogotá DataJam 2026.
