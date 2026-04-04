# move_file.py

# Tool Definition

import os
import shutil

from typing import Union

tool_definition = {
    "type": "function",
    "function": {
        "name": "move_file",
        "description": "Mueve o renombra un archivo desde una ruta de origen a una ruta de destino.",
        "parameters": {
            "type": "object",
            "properties": {
                "src": {
                    "type": "string",
                    "description": "Ruta del archivo origen."
                },
                "dest": {
                    "type": "string",
                    "description": "Ruta donde se moverá o renombrará el archivo."
                }
            },
            "required": ["src", "dest"]
        }
    }
}

# Function implementation

def run(src: str, dest: str) -> str:
    """Mueve o renombra el archivo de src a dest. Devuelve mensaje de éxito o error."""
    print(" ⚙️ Herramienta llamada: move_file")
    try:
        if not os.path.isfile(src):
            return f"Error en move_file: el archivo origen '{src}' no existe."
        dest_dir = os.path.dirname(dest)
        if dest_dir and not os.path.isdir(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
        shutil.move(src, dest)
        return f"Archivo movido de '{src}' a '{dest}'."
    except Exception as e:
        err = f'Error en move_file: {str(e)}'
        print(err)
        return err
