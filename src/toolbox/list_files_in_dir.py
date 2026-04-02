import os

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
    print(" ⚙️ Herramienta llamada: list_files_in_dir")
    try:
        files = os.listdir(directory)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}