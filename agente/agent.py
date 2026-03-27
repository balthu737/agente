import os
from memoria.simple_memory import SimpleMemory

class Agent:
    def __init__(self):
        self.setup_tools()
        self.memory = SimpleMemory()
        # self.messages = [
        #     {
        #         "role": "system",
        #         "content": "Sos un asistente que habla español y sos muy conciso con tus respuestas"
        #         }
        #     ]
        self.system_prompt = {
            "role": "system",
            "content": "Sos un asistente que habla español y sos muy conciso"
            }
    def setup_tools(self):
        self.tools =[
            {
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
    },
    {
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
    },
    {
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
    ]
        #herramienta
    def list_files_in_dir(self, directory="."):
        print(" ⚙️ Herramienta llamada: list_files_in_dir")
        try:
            files = os.listdir(directory)
            return {"files": files}
        except Exception as e:
            return {"error": str(e)}
    
    def read_file(self, path):
        print(" ⚙️ Herramienta llamada: read_file")
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            err = f'Error al leer el archivo {path}'
            print(err)
            return err
    
    def edit_file(self, path, prev_text, new_text):
        print(" ⚙️ Herramienta llamada: edit_file")
        try:
            existe = os.path.exists(path)
            if existe and prev_text:
                content = self.read_file
                
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
    
    def get_messages(self):
        msgs = [self.system_prompt]
        if self.memory.summary:
            msgs.append({
                "role": "system",
                "content": f"Información previa del usuario: {self.memory.summary}"
            })
        msgs += self.memory.memory[-6:]
        return msgs
    
    def process_response(self, response):
        #True = si llama a una funcion. False = No hubo llamado
        message = response.message
        
        # guardar respuesta del modelo en el historial
        self.memory.add("asistant", message.content)
        # self.messages.append({
        #     "role": "assistant",
        #     "content": message.content
        # })
        
        # verificar si quiere usar herramientas
        if message.tool_calls:
            for tool in message.tool_calls:
                fn_name = tool.function.name
                args = tool.function.arguments
                print(f'El esclavo quiere usar la herramienta: {fn_name}')
                print(f'Argumentos: {args}')
                if fn_name == "list_files_in_dir":
                    result = self.list_files_in_dir(**args)
                elif fn_name == "read_file":
                    result = self.read_file(**args)
                elif fn_name == "edit_file":
                    result = self.edit_file(**args)
                self.memory.add("tool", message.content)
                # self.messages.append({
                #     "role": "tool",
                #     "content": json.dumps(result)
                # })
            return True 
        else:
            print(f'Esclavo AI: {message.content}')
