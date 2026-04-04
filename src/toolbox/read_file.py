"""
:mod:`read_file`
================

Herramienta para leer el contenido de un archivo del sistema.

Permite acceder al contenido de archivos de texto dentro de una ruta específica.
Es utilizada por el agente para inspeccionar información almacenada en el workspace.

Esta herramienta accede al sistema de archivos, por lo que debe restringirse
a un entorno seguro (sandbox).
"""

tool_definition ={
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lee el contenido de un archivo en una ruta especifica",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directorio a leer"
                    }
                },
                "required": ["path"]
            }
        }
    }

def run(path):
    """
    Lee el contenido de un archivo de texto.

    Intenta abrir el archivo con codificación UTF-8 y devuelve su contenido.
    Si ocurre un error (archivo inexistente, permisos, etc.), devuelve un mensaje.

    :param path: Ruta del archivo a leer
    :type path: str

    :return: Contenido del archivo o mensaje de error
    :rtype: str

    Seguridad:
        - Puede acceder a archivos sensibles si no se restringe la ruta
        - No valida accesos fuera del workspace permitido

    Recomendaciones:
        - Limitar acceso a un directorio base (sandbox)
        - Validar rutas antes de abrir archivos
    """
    print(" ⚙️ Herramienta llamada: read_file")
    try:
        with open(path, encoding="utf-8") as f:
            return {"status": 200, "messages": f.read()}
    except Exception as e:
        err = f'Error al leer el archivo {path}'
        print(err)
        return {"status": 400, "messages": err}