from environs import Env
import requests
import html

env = Env()  
env.read_env()

def get_token():
    return env('TOKEN')

def get_channel_id():
    return env('CHANAL')

def send_news_to_telegram(data):
    description = html.unescape(data['info'])
    bold_header = f"<b>{data['message']}</b>"
    list_product = '\n'.join(data['items_list'])
    text = f"{bold_header}\n{description}\n{list_product}"

    try:
        response = requests.post(
            url=f'https://api.telegram.org/bot{get_token()}/sendMessage',
            json={'chat_id': get_channel_id(), 'text': text, 'parse_mode': 'HTML'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        return f"Ошибка отправки сообщения: {error}"
    
def send_activate_promo(data):
    title = f"<b>{data['title']}</b>"
    message = html.unescape(data['message'])
    text = f"{title}\n{message}"
    try:
        response = requests.post(
            url=f'https://api.telegram.org/bot{get_token()}/sendMessage',
            json={'chat_id': get_channel_id(), 'text': text, 'parse_mode': 'HTML'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        return f"Ошибка отправки сообщения: {error}"