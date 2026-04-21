import json
import os
import glob

NOTEBOOKS_DIR = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\02_notebooks\Analisis_Andres"

replacement_code_template = """# 1. Cargar Poblacion y Normalizar
    df_pob = pd.read_csv('../../01_datos/processed/p_poblacion_bogota.csv')
    df_pob['localidad_clean'] = df_pob['localidad'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    
    # 2. Limpiar columna de localidad original
    df_loc = df__{}_[{}_].dropna().astype(str).str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df_loc = df_loc.str.replace(r'^\\d+\\s*-\\s*', '', regex=True)
    
    # 3. Contar y Cruzar
    loc_counts = df_loc.value_counts().reset_index()
    loc_counts.columns = ['localidad_clean', 'casos']
    
    df_merged = loc_counts.merge(df_pob, on='localidad_clean', how='left')
    df_merged = df_merged[df_merged['poblacion'] > 0]
    
    # 4. Calcular Tasa por 100k
    df_merged['tasa_100k'] = (df_merged['casos'] / df_merged['poblacion']) * 100000
    df_merged = df_merged.sort_values('tasa_100k', ascending=False).head({head})
    
    # 5. Graficar
    plt.figure(figsize=(12,6))
    sns.barplot(x=df_merged['tasa_100k'], y=df_merged['localidad'], palette='{palette}')
    plt.title('{title}')
    plt.xlabel('Tasa por 100,000 Habitantes')
    plt.ylabel('Localidad')
    plt.show()
    
    print(f'Las localidades con mayor riesgo/cobertura relativa son:\\n', df_merged[['localidad', 'tasa_100k', 'casos']].head(3).to_string(index=False))"""

configs = {
    "05_Oferta_Cultura.ipynb" : {
        "df_name": "cultura",
        "col_name": "'localidad'",
        "head": 15,
        "palette": "husl",
        "title": "Tasa Cobertura Centros Culturales por 100k Habitantes",
        "old_marker": "densidad = df_cultura['localidad'].value_counts()"
    },
    "06_Riesgo_Consumo_SPA.ipynb" : {
        "df_name": "spa",
        "col_name": "'NOMBRELOCALIDADRESIDENCIA'",
        "head": 10,
        "palette": "inferno",
        "title": "Tasa de Riesgo de Consumo SPA por 100k Habitantes",
        "old_marker": "ranking_spa = df_spa['NOMBRELOCALIDADRESIDENCIA'].value_counts().head(10)"
    }
}

for nb_file in glob.glob(os.path.join(NOTEBOOKS_DIR, "*.ipynb")):
    basename = os.path.basename(nb_file)
    if basename in configs:
        cfg = configs[basename]
        
        with open(nb_file, "r", encoding="utf-8") as f:
            nb = json.load(f)
            
        modified = False
        for cell in nb.get("cells", []):
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                if cfg["old_marker"] in source:
                    new_code = replacement_code_template.format(
                        cfg["df_name"],
                        cfg["col_name"],
                        head=cfg["head"],
                        palette=cfg["palette"],
                        title=cfg["title"]
                    )
                    
                    lines = source.split("\\n")
                    new_lines = []
                    in_block = False
                    for line in lines:
                        if cfg["old_marker"] in line:
                            in_block = True
                            indent = line[:len(line) - len(line.lstrip())]
                            indented_code = "\\n".join([indent + l for l in new_code.split("\\n")])
                            new_lines.append(indented_code)
                            continue
                        
                        if in_block:
                            if line.strip() == "plt.show()" or line.strip() == "" or "print(" in line or "len(" in line or "baja_cobertura = " in line:
                                pass # Skip old plotting lines
                            else:
                                if line.strip() and not line.startswith(indent):
                                    in_block = False
                                    new_lines.append(line)
                        else:
                            new_lines.append(line)

                    if modified == False:
                        full_new_source = "\\n".join(new_lines)
                        cell["source"] = [l + "\\n" for l in full_new_source.split("\\n")]
                        if cell["source"][-1] == "\\n":
                            cell["source"] = cell["source"][:-1]
                        modified = True

        if modified:
            with open(nb_file, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=1)
            print(f"Updated {basename}")
