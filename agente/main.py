from ollama import chat
from agent import Agent

agent = Agent()
model ='gpt-oss'

while True:
    
    user_input = input("Yo: ").strip()
    
    #validacion
    if not user_input:
        continue
    
    if user_input.lower() in ("salir", "exit", "bye", "chau", "hasta la vista baby"):
        print("Adios!")
        break
    
    #historial
    agent.messages.append(
        {
            "role": "user",
            "content": user_input
            }
        )
    while True:
        #chat
        response = chat( 
            model=model,
            messages=agent.messages,
            tools=agent.tools
            )
        
        called_tool = agent.process_response(response)
        if not called_tool:
            break
