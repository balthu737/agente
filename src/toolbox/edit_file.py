import os 
from src.core.file_utils import read_file

tool_definition =     {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edita el contenido de un archivo reemplazando prev_text por new_text",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "La ruta del archivo a editar o crear"
                    },
                    "prev_text": {
                        "type": "string",
                        "description": "El texto que se va a buscar para reemplazaar (puede ser vacio)"
                    },
                    "new_text": {
                        "type": "string",
                        "description": "El texto que reemplaza a prev_text (o el texto para crear un archivo)"
                    },
                },
                "required": ["path", "new_text"]
            }
        }
    }

def run(path, prev_text, new_text):
    print(" ⚙️ Herramienta llamada: edit_file")
    try:
        existe = os.path.exists(path)
        if existe and prev_text:
            content = read_file(path)
            
            if prev_text not in content:
                return f'El texto {prev_text} no fue encontrado en el archivo'
            
            content = content.replace(prev_text, new_text)
        else:
            dir_name = os.path.dirname(path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            
            content = new_text
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        action = "editado" if existe and prev_text else "creado"
        return f'Archivo {path} {action} existosamente'
    except Exception as e:
        err = f'Error al crear o modificar el archivo {path}'
        print(err)
        return err