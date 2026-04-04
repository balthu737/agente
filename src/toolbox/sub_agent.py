from ollama import chat
from dotenv import load_dotenv
import os 

load_dotenv()
model_coder = os.getenv("model-coder")

class SubAgent:
    def __init__(self):
        self.sub_agent = {
            "coder": self.coder
        }
        self.tool_definition = {
            "coder": {
            "type": "function",
            "function": {
                "name": "coder",
                "description": "IA que genera codigo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instruction": {
                            "type": "string",
                            "description": "Instruccion para que la IA sepa que realizar"
                        }
                    },
                    "required": ["instruction"]
                }
            }
        }
}
    def coder(self, instruction):
        messages = instruction
        response = chat(
            model=model_coder,
            messages=[{"role": "user", "content": messages}]
        )
        result = response.message.content
        return result
