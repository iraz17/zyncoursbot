import requests
import os
import time
import requests
import logging
from dotenv import load_dotenv

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = '-1001328242392'

def envoyer_message_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {'chat_id': CHANNEL_ID, 'text': message, 'parse_mode': 'Markdown'}
    try:
        response = requests.post(url, json=params)
        response.raise_for_status()
        logger.info("Message envoyé avec succès à Telegram.")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message à Telegram : {e}")

def get_zynecoin_info():
    # Endpoint de l'API de CoinMarketCap pour le Zynecoin (remplacez "YOUR_API_KEY" par votre clé API)
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '1de437c0-f9cb-47d3-9361-e8b8592efcba',  # Remplacez par votre clé API CoinMarketCap
    }
    parameters = {
        'symbol': 'ZYN',  # Symbole du Zynecoin
    }

    try:
        # Envoyer une requête GET à l'API de CoinMarketCap
        response = requests.get(url, headers=headers, params=parameters)

        # Vérifier si la requête a réussi (code de statut 200)
        if response.status_code == 200:
            # Extraire les données JSON de la réponse
            data = response.json()

            # Extraire les informations pertinentes
            zyn_data = data['data']['ZYN']
            name = zyn_data['name']
            current_price = round(zyn_data['quote']['USD']['price'],3)

            market_cap = round(zyn_data['quote']['USD']['market_cap'],3)
            formatted_market_cap = "{:,.2f}".format(market_cap)
            volume_24h = round(zyn_data['quote']['USD']['volume_24h'],3)
            formatted_volume_24h  = "{:,.2f}".format(volume_24h )
            rank = zyn_data['cmc_rank']
            message_telegram = f"*{name}*\n*rang*:{rank}\n*Prix actuel* (USD): {current_price}\n*Capitalisation boursière* (USD): {formatted_market_cap}\n*Volume sur 24h* (USD): {formatted_volume_24h}"

            envoyer_message_telegram(message_telegram)

        else:
            print("Erreur: Impossible de récupérer les données du Zynecoin.")
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")

if __name__ == '__main__':
    while True:
        try:
            print("TELEGRAM_BOT_TOKEN:", TELEGRAM_BOT_TOKEN)
            get_zynecoin_info()
            # Attendez 4 heure (14400 secondes) avant de réexécuter la fonction
            time.sleep(14400)
        except Exception as e:
            break