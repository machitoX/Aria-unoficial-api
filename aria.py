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

while True:
    message = input('Escribe tu mensaje: ')
    
    if message.lower() == 'salir':
        break
    
    data = {
        "stream": True,
        "linkify": False,
        "conversation_id": None,
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
                except json.JSONDecodeError:
                    pass
        print('Respuesta del chat:', message)
        time.sleep(1)
    else:
        print(f'Error: {response.status_code}')
