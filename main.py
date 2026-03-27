from ollama import chat
from agente.agent import Agent

agent = Agent()
model ='gpt-oss:20b'

while True:
    
    user_input = input("Yo: ").strip()
    
    #validacion
    if not user_input:
        continue
    
    if user_input.lower() in ("salir", "exit", "bye", "chau", "hasta la vista baby"):
        print("Adios!")
        break
    
    #historial
    agent.memory.add("user", user_input)
    # agent.messages.append(
    #     {
    #         "role": "user",
    #         "content": user_input
    #         }
    #     )
    while True:
        #chat
        response = chat( 
            model=model,
            messages=agent.get_messages(),
            tools=agent.tools
            )
        
        called_tool = agent.process_response(response)
        if not called_tool:
            break
