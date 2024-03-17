import requests
import html

def get_token():
    return '7179574801:AAEuYIguGopcPh8HzJwhvv2yOI349sUMV2s'

def get_channel_id():
    return '-1002083926678'

def send_news_to_telegram(data):
    description = html.unescape(data['message'])
    bold_header = f"<b>{data['info']}</b>"
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