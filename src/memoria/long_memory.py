from ollama import chat
from dotenv import load_dotenv
import os 
load_dotenv()

model = os.getenv("model-memory")

class LongMemory:
    def __init__(self):
        pass
    def experience_memory(self, old_summarys):
        prompt = (
            f"""
            Tu tarea es crear una experiencia a partir de los resumenes del asistente
            {old_summarys}
            Genera una una experiencia en la que se guardan datos clave
            La experiencia debe ser corta, teniendo solo palabras claves.
            """
        )
        resp = chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        
        msg = resp.message
        return msg.content or ""