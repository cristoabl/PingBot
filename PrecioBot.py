import logging
import re
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import config

# Configura el nivel de registro y el token de tu bot de Telegram
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = config.tk


# URL base de la API de GeckoTerminal
GECKO_BASE_URL = 'https://api.geckoterminal.com/api/v2'

# Función para obtener información de un token desde GeckoTerminal
def get_token_info(contract_address):
    try:
        # Endpoint para obtener información de un token por dirección de contrato
        endpoint = f'/networks/eth/tokens/{contract_address}'
        headers = Accept: application/json;version=20230302

        # Realiza la solicitud GET a la API de GeckoTerminal
        response = requests.get(GECKO_BASE_URL + endpoint)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            token_data = response.json()
            # Procesa la información del token como desees
            token_name = token_data['name']
            token_symbol = token_data['symbol']
            return f"Nombre del Token: {token_name}\nSímbolo del Token: {token_symbol}\n\n"
        else:
            return "No se pudo obtener información del token."

    except Exception as e:
        return "Error al obtener información del token."

# Función para manejar el comando /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        fr"¡Hola, {user.mention_html()}!",
        reply_markup=None,
    )

# Función para manejar mensajes que contienen un contrato de token de Ethereum
def handle_token_contract(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    contract_match = re.search(r'0x[a-fA-F0-9]{40}', message_text)
    if contract_match:
        contract_address = contract_match.group(0)
        token_info = get_token_info(contract_address)
        if token_info:
            update.message.reply_text(token_info)
        else:
            update.message.reply_text("No se pudo encontrar información sobre ese token.")
    else:
        update.message.reply_text("No se encontró un contrato válido de token de Ethereum.")

def main() -> None:
    # Crea el objeto Updater de Telegram y pasa el token de tu bot
    updater = Updater(TOKEN)

    # Obtiene el objeto Dispatcher para registrar manejadores de comandos y mensajes
    dp = updater.dispatcher

    # Registra el manejador para el comando /start
    dp.add_handler(CommandHandler("start", start))

    # Registra el manejador para mensajes que contienen contratos de tokens de Ethereum
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'0x[a-fA-F0-9]{40}'), handle_token_contract))

    # Inicia el bot de Telegram
    updater.start_polling()

    # Ejecuta el bot hasta que se presione Ctrl+C para detenerlo
    updater.idle()

if __name__ == '__main__':
    main()
