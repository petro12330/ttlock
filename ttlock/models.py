from django.db import models
from django.conf import settings

class Ttlock(models.Model):
    """Замки"""

    lockId = models.CharField(verbose_name="Номер замка",
                                         max_length=35)
    client_secret = models.CharField(verbose_name="Секрет",
                                         max_length=35)
    clientId = models.CharField(verbose_name="Номер клиета",
                                         max_length=35)
    access_token = models.CharField(verbose_name="Аксес токен",
                                         max_length=35)
    refresh_token = models.CharField(verbose_name="Рефреш окен",
                                         max_length=35)
    address = models.CharField(verbose_name="Адрес",
                                         max_length=40)


class TtlockUser(models.Model):
    """Модель для обычных пользователей замка(не карта)."""

    lockId = models.ForeignKey(Ttlock, verbose_name="Номер замка",
                               on_delete=models.CASCADE)
    lockDate = models.CharField(verbose_name="Время последнего визита.",
                                         max_length=14, null=True)
    recordType = models.CharField(verbose_name="",
                                         max_length=14, null=True)
    phone = models.CharField(verbose_name="Номер телефона",
                             max_length=11, null=True)
    success = models.PositiveIntegerField(
        verbose_name="Статус открытия", null=True
    )
    keyboardPwd = models.CharField(verbose_name="Пароль",
                                         max_length=14)
    username = models.CharField(verbose_name="Имя/Номер пользователя",
                                         max_length=40)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lockId = models.ForeignKey(Ttlock, verbose_name="Номер замка",
                               on_delete=models.CASCADE)
