import json
import requests

"""
Скрипт запускается из консоли и нужен для локальной проверки отправки сообщений.
TODO: добавить кнопку для отправки тесового сообщения из интерфейса
"""

USER_PHONE = None
CHAT_2_DECK_TOKEN = "85b705d7d5d8f412074f11b1494a2b"
headers = {
    "Authorization": CHAT_2_DECK_TOKEN,
    "Content-Type": "application/json"
}
s = requests.Session()

CHAT_2_DECK_URL = "https://api.chat2desk.com/v1"


def response_to_json(response):
    return json.loads(response.text)


def get_or_create_id_user(phone):
    url = f"{CHAT_2_DECK_URL}/clients/?phone={phone}"
    response = s.get(url=url, headers=headers)
    response_data = response_to_json(response)
    if not response_data["data"]:
        payload = json.dumps({
            "phone": phone,
            "transport": "whatsapp"
        })
        url = f"{CHAT_2_DECK_URL}/clients"
        response = requests.request("POST", url, headers=headers,
                                    data=payload)
        response_data = response_to_json(response)
        return response_data["data"]["id"]

    return response_data["data"][0]["id"]


def send_message():
    if USER_PHONE is None:
        print('Напишите номер для отравки в переменную USER_PHONE')
    user_id_dialog = get_or_create_id_user(USER_PHONE)
    text = f"Сформировали для Вас счет. К оплате 1 рублей за Тест"
    url = f"{CHAT_2_DECK_URL}/messages?client_id={user_id_dialog}&text={text}"

    r = requests.request("POST", url, headers=headers)
    print(r.status_code)


send_message()
