import base64
import json
import uuid
from datetime import datetime
from pprint import pprint

from django.conf import settings
from requests import Session

from ttlock.services.chat2deck_service import send_message_by_phone

MESSAGE_TEXT = """🎁 Вам начислено {points} UDS
Итого UDS: {all_points}
Используйте их на практику английского!"""

UNDEFINED_USER_MESSAGE = """📥 *Скачайте приложение* https://okey.uds.app/c и копите баллы после каждой оплаты! Обменивайте их на разговорные клубы и другие занятия из "Практикума"!

🎁 Получите 4000 баллов за регистрацию!"""


def add_points_user(money: int, client_phone: int):
    # Добавление бонуснов для пользователя в UDS
    error = ""
    s = Session()
    api_key = str(f"{settings.UDS_COMPANY_ID}:{settings.UDS_API_KEY}")
    auth_string = base64.b64encode(api_key.encode('utf-8'))
    response = s.request(
        method='GET',
        url=f'{settings.UDS_API_URL}customers/find?code=456123&phone=%2b{client_phone}',
        headers={
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
            'Authorization': 'Basic ' + auth_string.decode("utf-8"),
            'X-Origin-Request-Id': str(uuid.uuid4()),
            'X-Timestamp': datetime.now().isoformat(),
        })
    if response.status_code == 404:
        send_message_by_phone(client_phone, UNDEFINED_USER_MESSAGE)
        return error, response.status_code, response.text
    if response.status_code != 200:
        return error, response.status_code, response.text
    try:
        response_json = response.json()
        participant = response_json['user']['participant']
        user_id = participant['id']
        rate = participant["membershipTier"]["rate"]
        points = int(float(money) / 100 * rate)
        all_points = int(float(participant["points"]) + points)

        response = s.request(
            method='POST',
            url=f'{settings.UDS_API_URL}operations/reward',
            headers={
                'Accept': 'application/json',
                'Accept-Charset': 'utf-8',
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + auth_string.decode("utf-8"),
                'X-Origin-Request-Id': str(uuid.uuid4()),
                'X-Timestamp': datetime.now().isoformat(),
            },
            data=json.dumps({
                'participants': [user_id, ],
                'points': points
            }),
        )
        if response.status_code == 202:
            send_message_by_phone(client_phone, MESSAGE_TEXT.format(points=points, all_points=all_points))
    except Exception as e:
        print(e)
        pass
    return error, response.status_code, response.text
