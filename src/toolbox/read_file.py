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
    print(" ⚙️ Herramienta llamada: read_file")
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        err = f'Error al leer el archivo {path}'
        print(err)
        return err