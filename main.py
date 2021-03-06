from base_ttlock_utils.base_lock import TTLock
from ttlock_last.settings import BASE_URL_ADDRESS
import datetime
import requests
import json
from time import sleep
from decouple import config

data_users = [
    {"clientId": "a6c471688b194acc82b60df98f24d548",
     "token": "da11736a65488437ef4c1123f73c06c8"
     },
    {"clientId": "ae8f30e62436437d9b8b0f7e4b0e0119",
     "token": "2462ff0b13df8cdc853c7d96072e82c2"
     },
    {"clientId": "cca62430f2044940903484404753623e",
     "token": "9051f79e717dc78b44467813f06567ef"
     },
]

s = requests.Session()
s.get(f'{BASE_URL_ADDRESS}login/')
USERNAME_ADMIN = config("USERNAME_ADMIN")
PASSWORD_ADMIN = config("PASSWORD_ADMIN")
csrftoken = s.cookies['csrftoken']

login_data = dict(username=USERNAME_ADMIN, password=PASSWORD_ADMIN,
                  csrfmiddlewaretoken=csrftoken, next='/')
r = s.post(f"{BASE_URL_ADDRESS}login/", data=login_data)


def get_locks(token, clientId):
    lock_client = TTLock(clientId, token)
    gateways = list(lock_client.get_gateway_generator())
    locks = []
    for gateway in gateways:
        locks += list(
            lock_client.get_locks_per_gateway_generator(
                gateway.get("gatewayId")))
    return locks, lock_client


def get_sleep_time():
    now = datetime.datetime.now()
    if 6 < now.hour <= 20:
        sleep_time = 360
    else:
        sleep_time = 3600
    return sleep_time


url = f"{BASE_URL_ADDRESS}api/test/"
now = datetime.datetime.now()

if 6 < now.hour <= 23:
    for user in data_users:
        try:
            locks, ttlock_client = get_locks(user["token"], user["clientId"])
            for lock in locks:
                response = ttlock_client.get_last_user_list(lock.get("lockId"))["list"]
                payload = json.dumps(response)
                response = s.post(url, data=payload, cookies=s.cookies)
                if response.status_code != 201:
                    print(response.status_code)
                    print(response.text)
            sleep(5)
        except Exception as e:
            print(f"???????????? ?????? ?????????????????????? ?? ?????????? {user}")
            print(e)

