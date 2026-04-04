import os 
from core.file_utils import read_file

"""
Herramienta para crear o editar archivos dentro del sistema.

Permite crear archivos nuevos o reemplazar texto existente en archivos.

.. warning::
    Modifica el sistema de archivos directamente. Debe usarse con
    restricciones de sandbox. No valida rutas fuera del workspace.
"""

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
    """Crea o edita un archivo en el sistema de archivos.

    Si el archivo existe y ``prev_text`` está definido, busca ese texto
    y lo reemplaza por ``new_text``. Si el archivo no existe o ``prev_text``
    está vacío, crea el archivo con ``new_text`` como contenido.

    :param path: Ruta del archivo a editar o crear.
    :type path: str
    :param prev_text: Texto a buscar para reemplazo (opcional).
    :type prev_text: str
    :param new_text: Texto nuevo o contenido completo del archivo.
    :type new_text: str
    :returns: Mensaje indicando el resultado de la operación.
    :rtype: str

    .. warning::
        No valida que ``path`` esté dentro del workspace permitido.
        Agregar validación de sandbox antes de usar en producción.
    """
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
        return {"status": 200, "messages": "Archivo creado"}
    except Exception as e:
        err = f'Error al crear o modificar el archivo {path}'
        print(err)
        return {"status": 400, "messages": err}