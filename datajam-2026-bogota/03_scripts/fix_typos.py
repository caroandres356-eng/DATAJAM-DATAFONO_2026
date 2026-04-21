import json
import os
import glob

NOTEBOOKS_DIR = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\02_notebooks\Analisis_Andres"

replacements_dict = {
    "df__ideacion_['localidad_residencia'_]": "df_ideacion['localidad_residencia']",
    "df__suicidio_[col_loc_]": "df_suicidio[col_loc]",
    "df__deporte_[loc_name_]": "df_deporte[loc_name]",
    "df__cultura_['localidad'_]": "df_cultura['localidad']",
    "df__spa_['NOMBRELOCALIDADRESIDENCIA'_]": "df_spa['NOMBRELOCALIDADRESIDENCIA']"
}

for nb_file in glob.glob(os.path.join(NOTEBOOKS_DIR, "*.ipynb")):
    basename = os.path.basename(nb_file)
    with open(nb_file, "r", encoding="utf-8") as f:
        nb = json.load(f)
        
    modified = False
    for cell in nb.get("cells", []):
        if cell["cell_type"] == "code":
            # Combine source to a single string to fix line breaks
            source = "".join(cell["source"])
            old_s = source
            
            for k, v in replacements_dict.items():
                source = source.replace(k, v)
            
            # Fix split print statements:
            # Reconstruct print that got \n split
            if "print(f'Las localidades" in source:
                # Remove strange line breaks inside the print statement introduced by my split("\\n")
                new_src = []
                for line in source.split("\\n"):
                    if "print(f'Las local" in line and "', df_merged" not in line:
                        continue # Skip this line
                    if "', df_merged" in line and "to_string" in line:
                        # Reconstruct the line
                        indent = line[:len(line)-len(line.lstrip())]
                        reconstructed = indent + "print(f'Las localidades con mayor riesgo/cobertura relativa son:\\\\n', df_merged[['localidad', 'tasa_100k', 'casos']].head(3).to_string(index=False))"
                        new_src.append(reconstructed)
                    else:
                        new_src.append(line)
                
                source = "\\n".join(new_src)
                
            if old_s != source:
                # write back source
                cell["source"] = [l + "\\n" for l in source.split("\\n")]
                if cell["source"][-1] == "\\n":
                    cell["source"] = cell["source"][:-1]
                if cell["source"] and cell["source"][-1].endswith("\\n"):
                    cell["source"][-1] = cell["source"][-1][:-1]
                modified = True

    if modified:
        with open(nb_file, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"Fixed {basename}")
