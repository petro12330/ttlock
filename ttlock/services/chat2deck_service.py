import json

import requests

from django.conf import settings

headers = {
    "Authorization": settings.CHAT_2_DECK_TOKEN,
    "Content-Type": "application/json"
}
s = requests.Session()


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
    user_id_dialog = get_or_create_id_user(user_phone)
    text_message = f"{user.username} пришёл(а) на занятие в {user.lockDate}"
    url = f"{settings.CHAT_2_DECK_URL}messages?client_id={user_id_dialog}&text={text_message}"

    requests.request("POST", url, headers=headers)


def send_message_by_phone(phone, text_message):
    user_id_dialog = get_or_create_id_user(phone)
    url = f"{settings.CHAT_2_DECK_URL}messages?client_id={user_id_dialog}&text={text_message}"
    r = requests.request("POST", url, headers=headers)
    print(r)


def get_or_create_id_user(phone):
    url = f"{settings.CHAT_2_DECK_URL}clients/?phone={phone}"
    response = s.get(url=url, headers=headers)
    response_data = response_to_json(response)
    if response_data["data"]:
        return response_data["data"][0]["id"]

    payload = json.dumps({
        "phone": phone,
        "transport": "whatsapp"
    })
    url = f"{settings.CHAT_2_DECK_URL}clients"
    response = requests.request("POST", url, headers=headers,
                                data=payload)
    response_data = response_to_json(response)
    return response_data["data"]["id"]
