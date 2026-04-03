from ollama import chat
import sys
from dotenv import load_dotenv
import os 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from agente.agent import Agent

load_dotenv()
model_coder = os.getenv("model-coder")
memory = Agent()
class SubAgent:
    def __init__(self):
        self.sub_agent = {
            "coder": self.coder
        }
        self.tool_definition = {
            "type": "funcion",
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
        self.sub_agent_definition ={
            "coder_definition": self.tool_definition
        }
    def coder(self, instruction):
        message = instruction
        response = chat(
            model=model_coder,
            messages=message,
        )
        result = memory.process_response(response)