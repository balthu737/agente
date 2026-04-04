import os

"""
Herramienta para listar archivos dentro de un directorio.

Útil para explorar el workspace y entender la estructura de archivos disponible.

.. warning::
    Accede al sistema de archivos directamente. Limitar a un directorio
    base controlado para evitar exponer archivos sensibles.
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
    """Lista los archivos y carpetas dentro de un directorio.

    :param directory: Ruta del directorio a listar. Por defecto el directorio actual.
    :type directory: str
    :returns: Diccionario con lista de archivos en clave ``files``,
              o clave ``error`` con el mensaje si falla.
    :rtype: dict

    Ejemplo de retorno exitoso::

        {"files": ["archivo1.txt", "carpeta", "script.py"]}

    Ejemplo de retorno con error::

        {"error": "No such file or directory: '/ruta/inexistente'"}

    .. warning::
        No valida rutas fuera del entorno permitido.
    """
    print(" ⚙️ Herramienta llamada: list_files_in_dir")
    try:
        files = os.listdir(directory)
        return {"status": 200, "messages": files}
    except Exception as e:
        return {"status": 400, "messages": str(e)}