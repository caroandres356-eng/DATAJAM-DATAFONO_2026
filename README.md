# 🚀 Bogotá DataJam 2026: Análisis de Riesgo Suicida vs Oferta Institucional

Este repositorio contiene el proyecto desarrollado para el **Bogotá DataJam 2026**, enfocado en el análisis territorial de los factores de riesgo de salud mental y su relación con la oferta institucional en deporte y cultura en las localidades de Bogotá.

## 📝 Descripción del Problema
Bogotá enfrenta un aumento en los casos de ideación e intento de suicidio, particularmente en poblaciones jóvenes y territorios vulnerables. Este proyecto busca validar si existe una correlación entre la falta de acceso a programas institucionales (Deporte y Cultura) y el incremento del riesgo territorial, con el fin de proponer intervenciones focalizadas.

**Pregunta de Investigación:** ¿Cómo se relaciona la brecha de oferta institucional con el riesgo de suicidio y salud mental en las localidades de Bogotá?

---

## 📊 Fuentes de Datos
Todas las fuentes utilizadas provienen del portal de **DATOS ABIERTOS BOGOTÁ**, garantizando transparencia y reproducibilidad:

1.  **Salud - Suicidios**: Registros históricos de suicidios consumados (2015-2026).
2.  **Salud - Ideación**: Notificaciones de ideación e intento de suicidio (2012-2026).
3.  **Salud - Consumo SPA**: Registros de consumo de sustancias psicoactivas por localidad.
4.  **Oferta Deportiva**: Programas y oferta del Instituto Distrital de Recreación y Deporte (IDRD).
5.  **Oferta Cultural**: Centros culturales, bibliotecas y espacios de la Secretaría de Cultura.
6.  **Población**: Proyecciones poblacionales por localidad y año para normalización de tasas.

---

## 🛠 Metodología
El análisis se dividió en las siguientes fases:
1.  **Carga y Limpieza**: Estandarización de nombres de localidades, manejo de valores nulos y conversión de formatos (XLSX a CSV).
2.  **Análisis Territorial (Focal)**: Estudios individuales por cada dimensión (Salud, Deporte, Cultura, Habitabilidad).
3.  **Integración de Datos**: Cruce de fuentes para construir un dataset maestro por localidad/año.
4.  **Construcción de Índices**:
    *   **Índice de Riesgo**: Compuesto por tasas de suicidio, ideación y consumo SPA.
    *   **Índice de Oferta**: Compuesto por disponibilidad de programas deportivos y culturales.
5.  **Validación de Hipótesis**: Aplicación de modelos de regresión lineal para cuantificar la relación entre riesgo y oferta.
6.  **Modelado Predictivo**: Uso de modelos SARIMA y Holt-Winters para proyectar el riesgo futuro en territorios críticos como Ciudad Bolívar.

---

## 📂 Estructura del Repositorio
Siguiendo los lineamientos de la guía de entrega, el proyecto se organiza de la siguiente manera:

*   **[`01_datos/`](file:///c:/Users/Latitude/Documents/V%20Semestre/DATAJAM/DATAJAM-DATAFONO_2026/datajam-2026-bogota/01_datos/)**:
    *   `raw/`: Contiene los archivos originales en formato Excel (`.xlsx`) descargados de Datos Abiertos Bogotá.
    *   `processed/`: Versiones estandarizadas y normalizadas en formato CSV para carga rápida.
*   **[`02_notebooks/`](file:///c:/Users/Latitude/Documents/V%20Semestre/DATAJAM/DATAJAM-DATAFONO_2026/datajam-2026-bogota/02_notebooks/)**:
    *   `01_exploracion/`: Análisis descriptivo inicial de las fuentes.
    *   `02_analisis_focal/`: Notebooks dedicados a profundizar en cada dimensión (Ideación, Suicidio, Habitabilidad, Deporte, Cultura, Consumo SPA).
    *   `03_analisis_final/`: El notebook **`04_analisis_territorial_foco.ipynb`**, que centraliza la validación de hipótesis y el modelado predictivo.
*   **[`03_scripts/`](file:///c:/Users/Latitude/Documents/V%20Semestre/DATAJAM/DATAJAM-DATAFONO_2026/datajam-2026-bogota/03_scripts/)**: Scripts de automatización para limpieza masiva y conversión de formatos.
*   **[`04_powerbi/`](file:///c:/Users/Latitude/Documents/V%20Semestre/DATAJAM/DATAJAM-DATAFONO_2026/datajam-2026-bogota/04_powerbi/)**: Archivos del tablero interactivo de visualización.
*   **[`05_outputs/`](file:///c:/Users/Latitude/Documents/V%20Semestre/DATAJAM/DATAJAM-DATAFONO_2026/datajam-2026-bogota/05_outputs/)**: Tablas finales procesadas y resultados de las proyecciones.
*   **[`06_docs/`](file:///c:/Users/Latitude/Documents/V%20Semestre/DATAJAM/DATAJAM-DATAFONO_2026/datajam-2026-bogota/06_docs/)**: Documentación complementaria y fichas metodológicas.

---

## 📊 Acceso a Productos Finales

### 📈 Dashboard de Power BI
El tablero de control interactivo permite visualizar las brechas territoriales y las tendencias de riesgo.
*   **Ubicación**: [`04_powerbi/Dashborad_DataJam.pbix.zip`](file:///c:/Users/Latitude/Documents/V%20Semestre/DATAJAM/DATAJAM-DATAFONO_2026/datajam-2026-bogota/04_powerbi/)
*   *Nota*: Debe descomprimirse el archivo `.zip` para abrir el archivo `.pbix` en Power BI Desktop.

### 📑 Nota Técnica de Integración
El documento que detalla el proceso de limpieza, los retos técnicos y la metodología de unión de bases de datos se encuentra aquí:
*   **Ubicación**: [`06_docs/01_nota_tecnica_integracion.md`](file:///c:/Users/Latitude/Documents/V%20Semestre/DATAJAM/DATAJAM-DATAFONO_2026/datajam-2026-bogota/06_docs/01_nota_tecnica_integracion.md)

---

## ⚙️ Instrucciones de Ejecución
Para replicar el análisis, siga estos pasos:

1.  **Clonar el repositorio**:
    ```bash
    git clone [URL_DEL_REPOSITORIO]
    ```
2.  **Instalar dependencias**:
    Asegúrese de tener Python 3.10+ instalado.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecutar Notebooks**:
    Se recomienda iniciar con el notebook central:
    `02_notebooks/03_analisis_final/04_analisis_territorial_foco.ipynb`

---

## 👥 Equipo
*   **Julian Felipe Africano Preciado**
*   **Sebastián Gómez Román**
*   **Andres Felipe Caro Medina**
*   Participantes del Bogotá DataJam 2026.
