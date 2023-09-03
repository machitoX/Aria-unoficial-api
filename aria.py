import requests
import time
import json
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de AUTHORIZATION de las variables de entorno
AUTHORIZATION = os.environ.get('AUTHORIZATION')

# Importar el archivo config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Actualizar el valor de AUTHORIZATION en la configuración
config['headers']['Authorization'] = AUTHORIZATION

url = 'https://composer.opera-api.com/api/v1/a-chat'

conversation_id_file = 'conversation_id.txt'
if os.path.exists(conversation_id_file):
    with open(conversation_id_file, 'r') as f:
        conversation_id = f.read().strip()
else:
    conversation_id = None

while True:
    message = input('Escribe tu mensaje: ')
    
    if message.lower() == 'salir':
        with open(conversation_id_file, 'w') as f:
            f.write(conversation_id)
        break
    
    if message.lower() =='print':
        print(data)
    
    if message.lower() == 'reset':
        conversation_id = None
    
    data = {
        "stream": True,
        "linkify": False,
        "conversation_id": conversation_id,
        "query": message
    }
    
    response = requests.post(url, headers=config['headers'], data=json.dumps(data))
    if response.status_code == 200:
        lines = response.text.split('\n')
        message = ''
        for line in lines:
            if line.startswith('data:'):
                try:
                    data = json.loads(line[5:].strip())
                    if 'message' in data:
                        message += data['message']
                    if 'conversation_id' in data:
                        conversation_id = data['conversation_id']
                except json.JSONDecodeError:
                    pass
        print('Respuesta del chat:', message)
        time.sleep(1)
    else:
        print(f'Error: {response.status_code}')
