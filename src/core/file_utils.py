import os

def read_file(path):
    """
    Lee el contenido de un archivo de texto.

    Intenta abrir el archivo en modo lectura con codificación UTF-8 y devuelve
    su contenido como string. En caso de error (archivo inexistente, permisos,
    etc.), devuelve un mensaje descriptivo.

    :param path: Ruta del archivo a leer
    :type path: str

    :return: Contenido del archivo o mensaje de error
    :rtype: str

    :raises None: Los errores son capturados internamente y convertidos en texto

    ⚠️ Seguridad:
        - Validar que la ruta pertenezca a un directorio permitido (sandbox)
        - Evitar accesos a rutas sensibles del sistema
    """
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error al leer archivo: {str(e)}"