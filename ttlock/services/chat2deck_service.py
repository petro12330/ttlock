import json

import requests

from ttlock_last.settings import TOKEN

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}
s = requests.Session()

CHAT_DECK_URL = "https://api.chat2desk.com/v1/"


def response_to_json(response):
    return json.loads(response.text)


def retranslate_username(username):
    ru_alf = " абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    en_alf = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_username = ""
    n = 0

    for i in username:
        try:
            id_ang = en_alf.index(i)
            i_ru = ru_alf[id_ang]
        except Exception:
            new_username += i
            continue
        if n == 0:
            new_username += i_ru.upper()
            n = 1
            continue
        elif i == " ":
            n = 0
        new_username += i_ru

    return new_username


def send_message(user):
    user_phone = str(user.phone)
    # user_phone = "79964414976"
    user_id_dialog = get_or_create_id_user(user_phone)
    text = f"{user.username} пришёл(а) на занятие в {user.lockDate}"
    url = f"{CHAT_DECK_URL}messages?client_id={user_id_dialog}&text={text}"

    requests.request("POST", url, headers=headers)


def get_or_create_id_user(phone):
    url = f"{CHAT_DECK_URL}/clients/?phone={phone}"
    response = s.get(url=url, headers=headers)
    response_data = response_to_json(response)
    if not response_data["data"]:
        payload = json.dumps({
            "phone": phone,
            "transport": "whatsapp"
        })
        url = "https://api.chat2desk.com/v1/clients"
        response = requests.request("POST", url, headers=headers,
                                    data=payload)
        response_data = response_to_json(response)
        return response_data["data"]["id"]

    return response_data["data"][0]["id"]
