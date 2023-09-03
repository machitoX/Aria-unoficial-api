import requests
import time
import json
import telebot
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de BOT_TOKEN de las variables de entorno
BOT_TOKEN=os.environ.get("BOT_TOKEN")

# Obtener el valor de AUTHORIZATION de las variables de entorno
AUTHORIZATION = os.environ.get('AUTHORIZATION')

# Importar el archivo config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Actualizar el valor de AUTHORIZATION en la configuración
config['headers']['Authorization'] = AUTHORIZATION

url = 'https://composer.opera-api.com/api/v1/a-chat'

bot = telebot.TeleBot(BOT_TOKEN)

conversation_id = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hola! Soy un bot que puede interactuar con una ARIA OPERA")

@bot.message_handler(commands=['reset'])
def reset_chat(message):
    global conversation_id
    conversation_id = None
    bot.send_message(message.chat.id, "Se ha creado un nuevo chat.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    global conversation_id
    data = {
        "stream": True,
        "linkify": False,
        "conversation_id": conversation_id,
        "query": message.text
    }

    try:
        response = requests.post(url, headers=config['headers'], data=json.dumps(data))
    except requests.exceptions.ChunkedEncodingError as e:
        bot.send_message(message.chat.id, f'Error: {e}')
    
    if response.status_code == 200:
        lines = response.text.split('\n')
        message_text = ''
        for line in lines:
            if line.startswith('data:'):
                try:
                    data = json.loads(line[5:].strip())
                    if 'message' in data:
                        message_text += data['message']
                    if 'conversation_id' in data:
                        conversation_id = data['conversation_id']
                except json.JSONDecodeError:
                    pass
        bot.send_message(message.chat.id, message_text)
    else:
        bot.send_message(message.chat.id, f'Error: {response.status_code}')

try:
    bot.polling()
except Exception as e:
    print(f"Error: {e}")