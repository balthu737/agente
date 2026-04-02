import os 
from src.core.file_utils import read_file

"""
:mod:`edit_file`
================

Herramienta para crear o editar archivos dentro del sistema.

Permite:
- Crear archivos nuevos
- Reemplazar texto existente en archivos

⚠️ Esta herramienta modifica el sistema de archivos, por lo que debe usarse
con restricciones de seguridad (sandbox / workspace).
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
    """
    Crea o edita un archivo en el sistema de archivos.

    Comportamiento:
    - Si el archivo existe y `prev_text` está definido:
        - Busca `prev_text` en el contenido
        - Si lo encuentra, lo reemplaza por `new_text`
        - Si no lo encuentra, devuelve un error
    - Si el archivo no existe o `prev_text` está vacío:
        - Crea el archivo con `new_text` como contenido

    :param path: Ruta del archivo a editar o crear
    :type path: str

    :param prev_text: Texto a buscar para reemplazo (opcional)
    :type prev_text: str

    :param new_text: Texto nuevo o contenido completo del archivo
    :type new_text: str

    :return: Mensaje indicando el resultado de la operación
    :rtype: str

    :raises Exception: Captura cualquier error interno y devuelve mensaje de fallo

    ⚠️ Seguridad:
        - Puede sobrescribir archivos existentes
        - No valida rutas peligrosas (ej: fuera del workspace)
        - Riesgo de corrupción si se usa incorrectamente

    💡 Recomendación:
        - Validar que `path` esté dentro de un directorio permitido
        - Agregar confirmación antes de sobrescribir archivos críticos
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
        return f'Archivo {path} {action} existosamente'
    except Exception as e:
        err = f'Error al crear o modificar el archivo {path}'
        print(err)
        return err