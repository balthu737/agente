# list_files_recursive.py

# Tool Definition

from typing import List
import os

tool_definition = {
    "type": "function",
    "function": {
        "name": "list_files_recursive",
        "description": "Lista todos los archivos en un directorio y sus subdirectorios.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "La ruta del directorio que se desea listar."
                }
            },
            "required": ["directory"]
        }
    }
}

# Function implementation

def run(directory: str) -> List[str]:
    """Recorre recursivamente el directorio y devuelve la lista completa de archivos."""
    print(" ⚙️ Herramienta llamada: list_files_recursive")
    try:
        files = []
        for root, _, filenames in os.walk(directory):
            for f in filenames:
                files.append(os.path.join(root, f))
        return files
    except Exception as e:
        err = f'Error en list_files_recursive: {str(e)}'
        print(err)
        return err
