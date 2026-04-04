# delete_file.py

# Tool Definition

import os

from typing import Union

tool_definition = {
    "type": "function",
    "function": {
        "name": "delete_file",
        "description": "Elimina un archivo dado su ruta completa.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "La ruta absoluta o relativa del archivo que se desea eliminar."
                }
            },
            "required": ["path"]
        }
    }
}

# Function implementation

def run(path: str) -> str:
    """Intenta borrar el archivo especificado. Devuelve un mensaje de éxito o error."""
    print(" ⚙️ Herramienta llamada: delete_file")
    try:
        if not os.path.isfile(path):
            return f"Error en delete_file: el archivo '{path}' no existe."
        os.remove(path)
        return f"Archivo '{path}' eliminado correctamente."
    except Exception as e:
        err = f'Error en delete_file: {str(e)}'
        print(err)
        return err
