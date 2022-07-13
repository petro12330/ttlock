import json
import requests
from django.conf import settings
from utils import response_to_json
import re

headers = {
    "Authorization": settings.CHAT_2_DECK_TOKEN,
    "Content-Type": "application/json"
}
s = requests.Session()


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


def prepare_phone(phone):
    phone = re.sub('[ ()+-]', '', phone)
    phone = re.sub(f'{phone[0]}', '7', phone, 1)
    if len(phone) != 11:
        return None
    return phone
