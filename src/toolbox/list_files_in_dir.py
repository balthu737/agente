import os

"""
:mod:`list_files_in_dir`
========================

Herramienta para listar archivos dentro de un directorio.

Permite obtener el contenido de una carpeta del sistema de archivos.
Es útil para explorar el workspace y entender la estructura de archivos disponible.

⚠️ Esta herramienta accede al sistema de archivos, por lo que debe limitarse
a un entorno controlado (sandbox).
"""

tool_definition ={
    "type": "function",
    "function": {
        "name": "list_files_in_dir",
        "description": "Lista los archivos en un directorio",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directorio a listar"
                }
            },
            "required": []
        }
    }
}

def run(directory="."):
    """
    Lista los archivos y carpetas dentro de un directorio.

    :param directory: Ruta del directorio a listar (por defecto el actual)
    :type directory: str

    :return: Diccionario con la lista de archivos o un error
    :rtype: dict

    Estructura de retorno:
        - Éxito:
            {
                "files": ["archivo1.txt", "carpeta", ...]
            }

        - Error:
            {
                "error": "mensaje de error"
            }

    ⚠️ Seguridad:
        - Puede exponer archivos sensibles si no se restringe el acceso
        - No valida rutas fuera del entorno permitido

    💡 Recomendaciones:
        - Limitar el acceso a un directorio base (workspace)
        - Filtrar archivos ocultos o sensibles si es necesario
    """
    print(" ⚙️ Herramienta llamada: list_files_in_dir")
    try:
        files = os.listdir(directory)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}