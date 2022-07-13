from ttlock_last.settings import BASE_URL_ADDRESS
import requests

s = requests.Session()

url = "https://ci34005.tmweb.ru/api/write_list_notify_group"

s.get(f'{BASE_URL_ADDRESS}api/write_list_notify_group')

response = requests.request("GET", url)

print(response.text)
