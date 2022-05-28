import json


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
