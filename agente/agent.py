import importlib
import os
from memoria.simple_memory import SimpleMemory

class Agent:
    def __init__(self):
        self.tools = []
        self.tool_map = {}
        
        self.load_tools()
        
        self.memory = SimpleMemory()
        self.system_prompt = {
            "role": "system",
            "content": "Sos un asistente que habla español y sos muy conciso"
            }
        
    def get_messages(self):
        msgs = [self.system_prompt]
        if self.memory.summary:
            msgs.append({
                "role": "system",
                "content": f"Información previa del usuario: {self.memory.summary}"
            })
        msgs += self.memory.memory[-6:]
        return msgs
    
    def load_tools(self):
        toolbox_path = os.path.join(os.path.dirname(__file__), "..", "toolbox")
        for file in os.listdir(toolbox_path):
            if file.endswith(".py") and file != "__init__.py":
                module_name = f"toolbox.{file[:-3]}"
                
                module = importlib.import_module(module_name)
                # definición para el modelo
                self.tools.append(module.tool_definition)
                # función ejecutable
                tool_name = module.tool_definition["function"]["name"]
                self.tool_map[tool_name] = module.run
    
    def process_response(self, response):
        #True = si llama a una funcion. False = No hubo llamado
        message = response.message
        
        # guardar respuesta del modelo en el historial
        self.memory.add("assistant", message.content)
        # self.messages.append({
        #     "role": "assistant",
        #     "content": message.content
        # })
        
        # verificar si quiere usar herramientas
        if message.tool_calls:
            for tool in message.tool_calls:
                fn_name = tool.function.name
                args = tool.function.arguments
                print(f'La IA quiere usar la herramienta: {fn_name}')
                print(f'Argumentos: {args}')
                if fn_name in self.tool_map:
                    try:
                        result = self.tool_map[fn_name](**args)
                    except Exception as e:
                        result = f"Error ejecutando la herramienta: {str(e)}"
                else:
                    result = f"Herramienta {fn_name} no encontrada"
                # if fn_name == "list_files_in_dir":
                #     result = self.list_files_in_dir(**args)
                # elif fn_name == "read_file":
                #     result = self.read_file(**args)
                # elif fn_name == "edit_file":
                #     result = self.edit_file(**args)
                self.memory.add("tool", message.content)
            return True 
        else:
            print(f'IA: {message.content}')
