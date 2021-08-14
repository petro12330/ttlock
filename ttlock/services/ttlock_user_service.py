import time
from datetime import datetime

from ttlock import models
from ttlock.services.chat2deck_service import send_message, retranslate_username


def translate_username(username):
    ru_alf = " абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    en_alf = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_username = ""
    for i in username:
        id_ru = ru_alf.find(i.lower())
        new_username += en_alf[id_ru]
    return new_username


def get_ttlock(user):
    return models.Ttlock.objects.get(
        profile__user=user
    )


def get_user_data(user_info):
    hours_3 = 10800  # Погрешность в 3 часа при переводе форматов
    username_en = str(user_info["username"])
    username_ru = retranslate_username(username_en)
    lockDate = str(datetime.utcfromtimestamp(
        int(str(user_info["serverDate"])[:-3]) + hours_3).strftime(
        "%H:%M  %d.%m.%Y"))
    keyboardPwd = str(user_info["keyboardPwd"])
    success = str(user_info["success"])
    return username_en, username_ru, lockDate, keyboardPwd, success


def get_user(ttlock, username_ru, lockDate, keyboardPwd):

    try:
        user = models.TtlockUser.objects.get(
            lockId_id=ttlock.id,
            keyboardPwd=keyboardPwd,
            username=username_ru
        )
    except models.TtlockUser.DoesNotExist:
        print("Создал пользователя")
        user = models.TtlockUser.objects.create(
            lockId_id=ttlock.id,
            keyboardPwd=keyboardPwd,
            username=username_ru,
            lockDate=lockDate
        )
    return user


def encode_time(date):
    return time.strptime(date, "%H:%M  %d.%m.%Y")


def auto_users(data, request):
    ttlock = get_ttlock(request.user)
    for user_info in data:
        if user_info['username'] is None:
            continue
        username_en, username_ru, lockDate, keyboardPwd, success = get_user_data(
            user_info)

        # Проверка на успешное открытие
        if success != '1':
            continue

        user = get_user(ttlock, username_ru, lockDate, keyboardPwd)

        # Если пользователь добавлен с сайта или с приложения,
        # lockDate не проставлена.
        if user.lockDate is None:
            user.lockDate = lockDate
            user.save()
            continue

        if encode_time(user.lockDate) >= encode_time(lockDate):
            continue
        user.lockDate = lockDate
        user.save()
        if user.phone is None:
            continue
        send_message(user)
