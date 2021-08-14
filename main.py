from ttlock_last.settings import BASE_URL_ADDRESS
from ttlockio.ttlockwrapper import ttlock, constants
import datetime
import requests
import json
from time import sleep

clientId = "cca62430f2044940903484404753623e"
token = "df770940fe92c0cc4b771410a44de9fc"

s = requests.Session()
s.get(f'{BASE_URL_ADDRESS}login/')
csrftoken = s.cookies['csrftoken']
login_data = dict(username="admin", password="12345",
                  csrfmiddlewaretoken=csrftoken, next='/')
r = s.post(f"{BASE_URL_ADDRESS}login/", data=login_data)

ttlock = ttlock.TTLock(clientId, token)

gateways = list(ttlock.get_gateway_generator())

locks = []
for gateway in gateways:
    locks += list(
        ttlock.get_locks_per_gateway_generator(gateway.get("gatewayId")))


def get_sleep_time():
    now = datetime.datetime.now()
    if 6 < now.hour <= 20:
        sleep_time = 360
    else:
        sleep_time = 3600
    return sleep_time


url = f"{BASE_URL_ADDRESS}api/test/"
while True:
    for lock in locks:
        response = ttlock.get_last_user_list(lock.get("lockId"))["list"]

        payload = json.dumps(response)
        response = s.post(url, data=payload, cookies=s.cookies)
        sleep(10)
