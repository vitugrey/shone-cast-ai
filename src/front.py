# ============ Importação ============= #
import requests
import json

# ============ Constantes ============= #
AGENT_ID="copywrite-agent"
ENDPOINT_URL=f"http://localhost:7777/agents/{AGENT_ID}/runs"


# ============== Código =============== #
def get_response_stream(message:str):
	response = requests.post(
		url=ENDPOINT_URL,
		data={
			"message": message,
			"stream": True,
		},
		stream=True,
	)
	for line in response.iter_lines():
		if line:
			if line.startswith(b'data: '):
				data=line[6:]
				try:
					event =json.loads(data)
					yield event
				except json.JSONDecodeError:
					continue
				
def print_response_stream(message:str):
    for event in get_response_stream(message=message):
        event_type = event.get("event","")
        
        # print(event_type)

        if event_type == "RunStarted":
            print('Execução iniciada...')
            print("-"*50)
			
        elif event_type == "RunContent":
            content = event.get("content","")
            if content:
                print(content, end='', flush=True)
				
        elif event_type == "ToolCallStarted":
            tool = event.get("tool",{})
            tool_name = tool.get("tool_name","Unknown Tool")
            tool_args = tool.get("tool_args",{} )
            print(f'TOOL INICIADA: {tool_name}')
            print(f'ARGUMENTOS: {tool_args}')
            print("-"*50)
			
        elif event_type == "ToolCallCompleted":
            tool_name = event.get("tool",{}).get('tool_name','Unknown Tool')
            print(f'TOOL FINALIZADA: {tool_name}')
            print("-"*50)
			
        elif event_type == "RunCompleted":
            print('\nExecução finalizada.')
            print("-"*50)
            metrics = event.get("metrics",{})
            # if metrics:
            #     print(f"METRICAS: {json.dumps(metrics, indent=2)}")

			
# ============= Execução ============== #
if __name__ == "__main__":
    while True:
        message = input("Digite sua mensagem para o agente: ")
        print_response_stream(message=message)
