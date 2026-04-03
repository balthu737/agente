# Tool: list_files_recursive
# This tool lists all files in a directory and its subdirectories.
# It returns a list of relative file paths.

import os

# Tool definition

tool_definition = {
    "type": "function",
    "function": {
        "name": "list_files_recursive",
        "description": "Lists all files in the given directory and its subdirectories, returning a list of relative file paths.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The root directory to search for files."
                }
            },
            "required": ["directory"]
        }
    }
}

# Function implementation

def run(directory):
    print(" ⚙️ Herramienta llamada: list_files_recursive")
    try:
        if not os.path.isdir(directory):
            return f"Error: '{directory}' is not a directory or does not exist."
        files = []
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                # Create a relative path
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, directory)
                files.append(rel_path)
        return files
    except Exception as e:
        err = f'Error en list_files_recursive: {str(e)}'
        print(err)
        return err
