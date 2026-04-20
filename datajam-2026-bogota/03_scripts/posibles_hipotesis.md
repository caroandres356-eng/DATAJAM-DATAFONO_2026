# Hipótesis de investigación — DATAJAM 2026
## Bogotá: Salud mental, territorio y oferta institucional

---

## H1 · La brecha de letalidad y género

**Hallazgo:** Las mujeres representan el 65.3% de los casos de ideación suicida,
pero los hombres concentran el 76.6% de los suicidios consumados y el 74.5%
del consumo de SPA.

**Hipótesis:** Los programas actuales de detección temprana son efectivos
captando el riesgo femenino pero fallan sistemáticamente en alcanzar al perfil
masculino de alta letalidad. Los hombres no piden ayuda, no son detectados, y
cuando el sistema los encuentra ya es tarde.

**Gráfica soporte:** `e3_brecha_genero.png`, `e4_ciclo_vital_comparado.png`

---

## H2 · La paradoja de la oferta institucional

**Hallazgo:** Chapinero y Los Mártires tienen más de 700 casos de ideación por
cada 1.000 participantes en programas deportivos — el ratio más alto de la
ciudad. Kennedy, con 33k casos totales, tiene uno de los ratios más bajos (373).

**Hipótesis:** La oferta institucional de deporte y cultura no sigue al riesgo
territorial — se concentra donde ya hay infraestructura, no donde la demanda
de salud mental lo exige. La cobertura alta en Kennedy no implica efectividad;
implica que el riesgo desborda cualquier oferta disponible.

**Gráfica soporte:** `c1_eficiencia_oferta_deporte.png`, `g5_brecha_riesgo_oferta.png`

---

## H3 · El multiplicador de habitabilidad

**Hallazgo:** Usme tiene 7% de viviendas sin servicios básicos y 16k casos de
ideación. Ciudad Bolívar tiene 65% de rezago habitacional alto y 25k casos.
Ambas muestran correlación directa entre déficit estructural de vivienda y
volumen de crisis de salud mental.

**Hipótesis:** La precariedad habitacional actúa como estresor crónico que
amplifica la ideación suicida por encima de factores clínicos individuales.
No es que las personas estén enfermas — es que el entorno las enferma.

**Gráfica soporte:** `d2_rezago_vs_ideacion.png`, `d3_servicios_vs_ideacion.png`, `d4_hacinamiento_vs_prob_economico.png`

---

## H4 · El salto de letalidad en estratos medios

**Hallazgo:** Chapinero convierte el 3.65% de sus casos de ideación en suicidio
consumado — más del doble del promedio ciudad (1.70%). Usaquén convierte el
2.73%. Ambas son localidades de estrato 4-6 con volumen de ideación bajo pero
letalidad desproporcionadamente alta.

**Hipótesis:** En estratos medios y altos, el estigma social reduce la ideación
reportada pero aumenta la efectividad del acto suicida. La ausencia de redes
de apoyo comunal — típicas de barrios populares — deja a estas personas sin
contención en el momento crítico.

**Gráfica soporte:** `e1_tasa_conversion_suicidio.png`, `d1_estrato_vs_ideacion.png`

---

## H5 · La deuda post-pandemia

**Hallazgo:** En 2020 se registró una caída en casos en casi todas las
localidades — probable subregistro por confinamiento. Entre 2021 y 2023, Suba
pasó de 1.706 a 4.480 casos (+163%) y Kennedy de 2.151 a 4.492 (+109%).
Los niveles no han bajado desde entonces.

**Hipótesis:** Bogotá atraviesa una ola de cola post-pandemia donde el deterioro
económico y el aislamiento de 2020 se transformaron en crisis de salud mental
persistente y estructural entre 2022 y 2025. El sistema de salud mental
absorbió el shock inicial pero no la ola secundaria.

**Gráfica soporte:** `c4_evolucion_pandemia.png`, `g7_tendencia_top5.png`

---

## H6 · La cadena temporal de riesgo no intervenido

**Hallazgo:** La ideación se concentra en adolescencia (32.1%) y juventud
(31.6%), pero el suicidio consumado se concentra en adultez (44.2%). El
consumo SPA también pico en adultez y juventud.

**Hipótesis:** Existe una cadena temporal de riesgo no intervenido: adolescente
con ideación no detectada → joven con consumo SPA como mecanismo de escape →
adulto que consuma suicidio. Cada eslabón no intervenido alimenta el siguiente.
La ventana crítica de prevención es la adolescencia.

**Gráfica soporte:** `e4_ciclo_vital_comparado.png`, `c2_heatmap_factores_riesgo.png`

---

## H7 · Los tres perfiles territoriales de riesgo

**Hallazgo:** El análisis cruzado revela que no hay un solo patrón territorial
de riesgo sino al menos tres perfiles distintos con causas y soluciones diferentes.

| Perfil | Localidades | Característica |
|--------|-------------|----------------|
| Densidad + consumo | Kennedy, Suba, Bosa | Alto volumen por población, baja conversión |
| Vulnerabilidad estructural | Ciudad Bolívar, Usme | Rezago habitacional, sin servicios, zona de riesgo |
| Paradoja económica | Los Mártires, Santa Fe, Teusaquillo | Problemas económicos sin pobreza de vivienda visible |

**Hipótesis:** Una política pública uniforme para todas las localidades es
ineficiente por definición. Cada perfil requiere una intervención distinta:
oferta masiva en el primero, inversión en infraestructura en el segundo,
y redes de contención social en el tercero.

**Gráfica soporte:** `g5_brecha_riesgo_oferta.png`, `g6_riesgo_vs_oferta_barras.png`, `d5_zona_riesgo_vs_ideacion.png`

---

*Generado con datos del DATAJAM 2026 — Bogotá D.C.*
*Datasets: ideación suicida, suicidio consumado, consumo SPA, programas deportivos,*
*centros culturales, condiciones de habitabilidad (2019–2025)*

---

## H8 · La oferta institucional como detector, no solo como preventor

**Hallazgo:** La correlación entre oferta deportiva/cultural per capita e intentos
de suicidio es positiva (r=0.44 deporte, r=0.47 cultura, r=0.66 índice combinado).
Donde hay más oferta hay más intentos reportados, no menos.

**Hipótesis:** La oferta institucional no reduce directamente la ideación — actúa
como sistema de detección temprana. Las personas que participan en programas
deportivos y culturales tienen más contacto con el sistema institucional y son
detectadas antes de llegar al acto consumado. Las localidades con poca oferta
tienen subregistro severo: el riesgo existe pero no es visible hasta que es
demasiado tarde. Esto explica por qué Chapinero y Usaquén, con relativamente
poca oferta per capita, tienen las tasas de conversión a suicidio consumado
más altas de la ciudad.

**Implicación de política:** Expandir la oferta en zonas de bajo acceso no solo
previene — hace visible el riesgo oculto y permite intervención temprana.

**Gráfica soporte:** `g1_deporte_percap_vs_intentos.png`, `g2_cultura_percap_vs_intentos.png`,
`g3_indice_oferta_vs_intentos_percap.png`

---

## H9 · Mapa de prioridad de intervención por cuadrante

**Hallazgo:** Al cruzar tasa de intentos per capita vs índice de oferta institucional
per capita emergen 4 perfiles de localidad con necesidades completamente distintas.

| Cuadrante | Localidades | Prioridad | Acción |
|-----------|-------------|-----------|--------|
| Alto riesgo, baja oferta | Los Mártires, Usme, Ciudad Bolívar | URGENTE | Crear oferta nueva donde no existe |
| Alto riesgo, alta oferta | Chapinero, Tunjuelito, Rafael Uribe Uribe, San Cristóbal, Teusaquillo | REFORZAR | La oferta existe pero no alcanza o no llega a quien la necesita |
| Bajo riesgo, baja oferta | Suba, Usaquén, Engativá, Kennedy, Fontibón, Barrios Unidos | MONITOREAR | Riesgo contenido por redes sociales informales — vigilar tendencia post-pandemia |
| Bajo riesgo, alta oferta | Bosa, Puente Aranda, Antonio Nariño | MODELO | Estudiar qué hace bien esta oferta y replicarlo |

**Hipótesis:** Una política pública de salud mental en Bogotá que no diferencie
por cuadrante va a desperdiciar recursos — reforzando donde ya hay oferta
(naranja) e ignorando donde no hay nada (rojo). El cuadrante rojo es la
deuda histórica de la ciudad con sus localidades más vulnerables.

**Gráfica soporte:** `g4_cuadrantes_riesgo_oferta.png`

---

## H10 · La Candelaria y Santa Fe: el epicentro invisible de vulnerabilidad compuesta

**Hallazgo:** Al construir un índice de vulnerabilidad compuesta (joven + intento
real + problemas económicos + conflicto de pareja + maltrato), La Candelaria
(242 por 100k) y Santa Fe (207 por 100k) lideran por amplio margen — más del
doble del promedio ciudad (119 por 100k). Son localidades pequeñas que no
aparecen en los rankings de volumen total pero concentran la mayor densidad
de casos con múltiples factores de riesgo simultáneos.

**Hipótesis:** El centro histórico de Bogotá es el epicentro silencioso de la
crisis de salud mental. Su perfil — habitaciones de inquilinato, alta rotación
poblacional, consumo SPA en vía pública, ausencia de redes familiares estables
— crea las condiciones perfectas para que la vulnerabilidad se acumule sin ser
detectada ni atendida. La baja población hace que los números absolutos sean
pequeños, pero la concentración de riesgo por habitante es la más alta de
la ciudad.

**Gráfica soporte:** `h1_vulnerabilidad_compuesta.png`

---

## H11 · La habitabilidad no actúa sola — actúa en combinación

**Hallazgo:** El índice de precariedad habitacional combinado (rezago +
sin servicios + hacinamiento) tiene correlación baja con intentos de suicidio
(r=0.10). Pero al desagregarlo, el rezago habitacional alto sí muestra
correlación positiva (r=0.26) mientras que sin servicios (r=-0.03) y m²
por persona (r=-0.02) son prácticamente neutros.

**Hipótesis:** La habitabilidad no es un predictor lineal de salud mental —
es un modulador de contexto. El rezago habitacional (deterioro estructural
visible, sensación de abandono estatal) tiene efecto psicológico directo.
En cambio la falta de servicios básicos o el hacinamiento, cuando son
la norma histórica de una comunidad, son normalizados y no generan el mismo
estresor agudo. Lo que enferma no es la pobreza absoluta sino la percepción
de deterioro relativo y abandono.

**Gráfica soporte:** `h4_componentes_habitabilidad.png`, `h3_habitabilidad_vs_intentos.png`

---

## H12 · El perfil vulnerable predice el suicidio consumado (r=0.48)

**Hallazgo:** El porcentaje de casos con perfil de máxima vulnerabilidad
por localidad tiene correlación de 0.48 con la tasa de suicidio consumado.
Chapinero y Santa Fe son los outliers más importantes — están muy por encima
de la línea de tendencia, lo que significa que su tasa de suicidio consumado
es mayor de lo que el perfil de vulnerabilidad explicaría.

**Hipótesis:** El perfil compuesto (joven + intento + factores sociales)
es un predictor moderado del suicidio consumado, pero no explica todo.
Los casos de Chapinero y Santa Fe que superan la tendencia sugieren que
hay un factor adicional no capturado — posiblemente el aislamiento social
de estratos medios-altos que no buscan ayuda aunque tengan el perfil de
riesgo. La vulnerabilidad compuesta es necesaria pero no suficiente para
predecir la letalidad: el acceso a redes de contención es el factor que
falta en el modelo.

**Gráfica soporte:** `h2_vuln_vs_suicidio.png`