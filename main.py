from ollama import chat
import sys
from dotenv import load_dotenv
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from agente.agent import Agent

load_dotenv()

workspace_env = os.getenv("workspace")

if os.path.isabs(workspace_env):
    workspace = workspace_env
else:
    workspace = os.path.join(os.path.dirname(__file__), workspace_env)
agent = Agent(workspace)
model = os.getenv("model")

"""
Script principal para ejecutar el agente conversacional en modo interactivo.

Este script:
- Inicializa el agente
- Maneja la entrada del usuario por consola
- Mantiene el historial de conversación
- Envía mensajes al modelo
- Permite la ejecución iterativa de herramientas

Flujo general:
1. El usuario ingresa un mensaje
2. Se guarda en memoria
3. Se envía al modelo junto con el contexto
4. El modelo responde
5. Si solicita herramientas, se ejecutan
6. Se repite hasta que no haya más tool calls
"""

while True:
    """
    Bucle principal de interacción con el usuario.

    Permite mantener una conversación continua hasta que el usuario decida salir.
    """
    
    user_input = input("Alejo: ").strip()
    
    #validacion
    if not user_input:
        continue
    
    if user_input.lower() in ("salir", "exit", "bye", "chau", "hasta la vista baby"):
        print("Adios!")
        break
    
    #historial
    agent.memory.add("user", user_input)
    while True:
        """
        Bucle interno de procesamiento del agente.

        Este loop permite:
        - Ejecutar múltiples herramientas en cadena
        - Reconsultar al modelo después de cada ejecución
        - Finalizar cuando el modelo ya no necesita herramientas
        """
        response = chat( 
            model=model,
            messages=agent.get_messages(),
            tools=agent.tools
            )
        
        called_tool = agent.process_response(response)
        if not called_tool:
            break
