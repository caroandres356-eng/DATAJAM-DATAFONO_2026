import json
import os
import glob

def convert_ipynb_to_py(notebook_path, output_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    code_lines = []
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            code_lines.extend(cell['source'])
            code_lines.append('\n\n')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(code_lines)

def process_all():
    source_dir = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\03_scripts\03.1_Cargaylimpieza"
    target_dir = r"c:\Users\Latitude\Documents\V Semestre\DATAJAM\DATAJAM-DATAFONO_2026\datajam-2026-bogota\03_scripts"
    
    notebooks = glob.glob(os.path.join(source_dir, "*.ipynb"))
    
    for nb_path in notebooks:
        filename = os.path.basename(nb_path).replace(".ipynb", ".py")
        # Rename n_ to s_ or just keep n_? User said "deja los notebooks... en .py"
        # I'll rename them to s_ (script) or just replace extension. User used "n_" for notebook.
        # I'll use "s_" for script to follow the pattern or just replace extension.
        # Let's use the filenames provided by replacing extension first.
        output_name = filename.replace("n_", "s_") 
        output_path = os.path.join(target_dir, output_name)
        
        print(f"Converting {nb_path} -> {output_path}")
        convert_ipynb_to_py(nb_path, output_path)

if __name__ == "__main__":
    process_all()
