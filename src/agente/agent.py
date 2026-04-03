import importlib
import os
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from memoria.simple_memory import SimpleMemory
from core.security import Security

class Agent:
    """
    Representa un agente autónomo con capacidades de memoria y uso de herramientas.

    Este agente:
    - Mantiene un historial de conversación (memoria de corto plazo).
    - Puede resumir contexto previo (memoria de largo plazo).
    - Carga herramientas dinámicamente desde un directorio.
    - Decide cuándo ejecutar herramientas en base a la respuesta del modelo.

    Está diseñado para actuar como un asistente personal enfocado en la toma de decisiones,
    resolución de problemas y ejecución de tareas de forma eficiente.
    """
    def __init__(self, workspace):
        """
        Inicializa el agente.

        Configura:
        - Lista de herramientas disponibles (`tools`)
        - Mapa de funciones ejecutables (`tool_map`)
        - Sistema de memoria (`SimpleMemory`)
        - Prompt base del sistema (personalidad y reglas del agente)

        Además, carga automáticamente las herramientas desde el directorio `toolbox`.
        """
        self.tools = []
        self.tool_map = {}
        
        self.load_tools()
        self.workspace = workspace
        self.security = Security(self.workspace)
        
        self.memory = SimpleMemory()
        self.system_prompt = {
            "role": "system",
            "content": f"""
            Tu nombre es Balthu.
            Mi nombre es alejo.
            Podes guardar y modificar los archivos de la carpeta {self.workspace}.
            Si la tool que estas usando devuelve un mensaje con la palabra exito o una respuesta valida,
            entonces no debes volver a ejecutar la accion,
            en caso contrario que devuelda otra cosa si volver a ejecutar la accion.
            """
            }
        
    def get_messages(self):
        """
        Construye la lista de mensajes que se enviarán al modelo.

        Incluye:
        - El prompt del sistema
        - Un resumen previo del usuario (si existe)
        - Los últimos mensajes de la conversación (memoria reciente)

        :return: Lista de mensajes en formato esperado por el modelo
        :rtype: list
        """
        msgs = [self.system_prompt]
        if self.memory.summary:
            msgs.append({
                "role": "system",
                "content": f"Información previa del usuario: {self.memory.summary}"
            })
        msgs += self.memory.memory[-6:]
        return msgs
    
    def load_tools(self):
        """
        Carga dinámicamente las herramientas desde el directorio `toolbox`.

        Por cada archivo Python encontrado:
        - Importa el módulo
        - Extrae la definición de la herramienta (`tool_definition`)
        - Registra la función ejecutable (`run`) en `tool_map`

        Requisitos de cada tool:
        - Debe tener `tool_definition`
        - Debe tener una función `run`

        :raises ImportError: Si algún módulo no puede ser importado
        :raises AttributeError: Si falta `tool_definition` o `run`
        """
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
        """
        Procesa la respuesta generada por el modelo.

        Funcionalidades:
        - Guarda la respuesta en memoria
        - Detecta si el modelo quiere usar herramientas
        - Ejecuta las herramientas solicitadas
        - Guarda los resultados en memoria

        :param response: Respuesta generada por el modelo (incluye mensaje y posibles tool_calls)
        :type response: object

        :return: 
            - True si se ejecutó al menos una herramienta
            - False si no hubo llamadas a herramientas
        :rtype: bool

        :raises Exception: Si ocurre un error durante la ejecución de una herramienta
        """
        #True = si llama a una funcion. False = No hubo llamado
        message = response.message
        
        # guardar respuesta del modelo en el historial
        self.memory.add("assistant", message.content)
        # verificar si quiere usar herramientas
        if message.tool_calls:
            for tool in message.tool_calls:
                fn_name = tool.function.name
                args = tool.function.arguments
                path = args.get("path", None)
                print(f'La IA quiere usar la herramienta: {fn_name}')
                print(f'Argumentos: {args}')
                if fn_name in self.tool_map:
                    try:
                        danger = self.security.authorization(fn_name, path)
                        if danger == "authorized":
                            result = self.tool_map[fn_name](**args)
                        else: 
                            result = f'La herramienta, {fn_name}, no fue autorizada'
                    except Exception as e:
                        result = f"Error ejecutando la herramienta: {str(e)}"
                else:
                    result = f"Herramienta {fn_name} no encontrada"
                self.memory.add("tool", str(result))
            return True 
        else:
            print(f'IA: {message.content}')
