from ollama import chat
import json

class SimpleMemory:
    def __init__(self, max_messeges:int=12, num_summarize:int=4):
        self.memory = []
        self.max_messeges = max_messeges
        self.num_summarize = num_summarize
        self.summary = ""
        self._load_json()
    
    def add(self, role:str, text:str):
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
        msgs = []
        
        if self.summary:
            msgs.append({
                "role": "system",
                "content": f"Memoria previa: {self.summary}"
            })
            
        return msgs + self.memory
    
    def summary_memory(self, old_memories):
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
            model="mistral:latest",
            messages=[{"role": "user", "content": prompt}]
        )
        msg = resp.message
        return msg.content or ""
    
    def _save_json(self, filename:str = "memory.json"):
        data = {
            "summary": self.summary,
            "memory": self.memory
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    def _load_json(self, filename: str = "memory.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.summary = data.get("summary", "")
                self.memory = data.get("memory", [])
        except FileNotFoundError:
            # primera ejecución → no pasa nada
            self.summary = ""
            self.memory = []