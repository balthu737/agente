from ollama import chat
import json
from dotenv import load_dotenv
import os

load_dotenv()

model = os.getenv("model-memory")
class ShortMemory:
    """
    Sistema de memoria híbrida para un agente conversacional.

    Combina:
    - Memoria de corto plazo (mensajes recientes)
    - Memoria de largo plazo (resumen consolidado)

    Funcionalidades principales:
    - Almacenar mensajes en orden cronológico
    - Resumir automáticamente mensajes antiguos cuando se supera un límite
    - Persistir la memoria en un archivo JSON
    - Recuperar estado previo al iniciar

    Este enfoque permite mantener contexto relevante sin sobrecargar el modelo.
    """
    def __init__(self, max_messeges:int=12, num_summarize:int=4):
        """
        Inicializa el sistema de memoria.

        :param max_messeges: Cantidad máxima de mensajes en memoria antes de resumir
        :type max_messeges: int

        :param num_summarize: Cantidad de mensajes a resumir cuando se supera el límite
        :type num_summarize: int
        """
        self.memory = []
        self.max_messeges = max_messeges
        self.num_summarize = num_summarize
        self.summary = ""
        self._load_json()
    
    def add(self, role:str, text:str, tool_calls=None):
        """
        Agrega un nuevo mensaje a la memoria.

        Si se supera el límite de mensajes:
        - Extrae los mensajes más antiguos
        - Genera un resumen con ellos
        - Actualiza la memoria de largo plazo

        :param role: Rol del mensaje ("user", "assistant", "tool", etc.)
        :type role: str

        :param text: Contenido del mensaje
        :type text: str
        """
        if tool_calls:
            self.memory.append({
                "role": role,
                "content": text,
                "tool_calls": tool_calls
            })
        else:
            self.memory.append({
                "role": role,
                "content": text
            })
        if len(self.memory) > self.max_messeges:
            print(f'Procesando resumen para {self.num_summarize} mensajes')
            
            to_summarize = self.memory[:self.num_summarize]
            self.memory = self.memory[self.num_summarize:]
            
            self.summary = self.summary_memory(to_summarize)
        self._save_json()
    
    def messages(self):
        """
        Construye la lista de mensajes para enviar al modelo.

        Incluye:
        - El resumen previo como contexto (si existe)
        - La memoria reciente

        :return: Lista de mensajes estructurados
        :rtype: list
        """
        msgs = []
        
        if self.summary:
            msgs.append({
                "role": "system",
                "content": f"Memoria previa: {self.summary}"
            })
            
        return msgs + self.memory
    
    def summary_memory(self, old_memories):
        """
        Genera un resumen consolidado de mensajes antiguos.

        Utiliza un modelo de lenguaje para:
        - Combinar el resumen anterior con nuevos mensajes
        - Mantener información clave (nombres, decisiones, contexto relevante)
        - Reducir la longitud del historial

        :param old_memories: Lista de mensajes a resumir
        :type old_memories: list

        :return: Nuevo resumen generado
        :rtype: str
        """
        summary_line = f'Resumen anterior: {self.summary} \n' if self.summary else "No hay resumen previo. \n"
        prompt = (
            f'Tu tarea es actualizar la memoria resumen del asistente\n'
            + summary_line +
            f'Nuevos mensajes a integrar: {old_memories}\n'
            f'Genera un nuevo resumen corto y consolidado que combine ambos,'
            f'manteniendo datos clave (nombres, acuerdos, fechas).\n'
            f'Guarda solo los datos importantes del usuario de manera muy consisa y estructurada.\n'
            f'El texto de resumen debe ser corto'
        )
        
        resp = chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        msg = resp.message
        return msg.content or ""
    
    def _save_json(self, filename:str = "memory.json"):
        """
        Guarda el estado actual de la memoria en un archivo JSON.

        Incluye:
        - Resumen consolidado
        - Mensajes recientes

        :param filename: Nombre del archivo de almacenamiento
        :type filename: str

        Nota:
            El archivo se sobrescribe en cada guardado.
        """
        data = {
            "summary": self.summary,
            "memory": self.memory
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    def _load_json(self, filename: str = "memory.json"):
        """
        Carga la memoria desde un archivo JSON si existe.

        Si el archivo no existe:
        - Inicializa memoria vacía
        - No lanza error

        :param filename: Nombre del archivo a cargar
        :type filename: str
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.summary = data.get("summary", "")
                self.memory = data.get("memory", [])
        except FileNotFoundError:
            # primera ejecución → no pasa nada
            self.summary = ""
            self.memory = []