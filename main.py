from ttlockio import ttlockwrapper
import datetime
import requests
import json
from time import sleep

clientId = "cca62430f2044940903484404753623e"
token = "df770940fe92c0cc4b771410a44de9fc"

s = requests.Session()
s.get('http://ci34005-django.tw1.ru/login/')
csrftoken = s.cookies['csrftoken']
login_data = dict(username="admin", password="1234554321",
                  csrfmiddlewaretoken=csrftoken, next='/')
r = s.post("http://ci34005-django.tw1.ru/login/", data=login_data)

ttlock = ttlockwrapper.TTLock(clientId, token)

gateways = list(ttlock.get_gateway_generator())

locks = []
for gateway in gateways:
    locks += list(
        ttlock.get_locks_per_gateway_generator(gateway.get("gatewayId")))


def get_sleep_time():
    now = datetime.datetime.now()
    if now.hour > 6 and now.hour <= 20:
        sleep_time = 360
    else:
        sleep_time = 3600
    return sleep_time


url = "http://ci34005-django.tw1.ru/api/test/"
while True:
    for lock in locks:
        response = ttlock.get_last_user_list(lock.get("lockId"))["list"]

        payload = json.dumps(response)
        response = s.post(url, data=payload, cookies=s.cookies)
        print(response.status_code)
        sleep(get_sleep_time())
