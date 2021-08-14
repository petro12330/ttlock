import random
import string

from ttlockio.ttlockwrapper import ttlock, constants
import datetime
import requests
import json
from time import sleep
from django.test import TestCase
from django.test import Client
from . import models
import uuid
from django.contrib.auth import get_user_model


def create_lock():
    return models.Ttlock.objects.create(
        lockId=''.join(random.sample(string.ascii_lowercase, 8)),
        client_secret=''.join(random.sample(string.ascii_lowercase, 8)),
        clientId=''.join(random.sample(string.ascii_lowercase, 8)),
        access_token=''.join(random.sample(string.ascii_lowercase, 8)),
        refresh_token=''.join(random.sample(string.ascii_lowercase, 8)),
        address=''.join(random.sample(string.ascii_lowercase, 8)),
    )


def create_profile(lock=True):
    username = ''.join(random.sample(string.ascii_lowercase, 8))
    password = ''.join(random.sample(string.ascii_lowercase, 8))
    user = get_user_model().objects.create_user(username=username,
                                                password=password)
    if lock:
        models.Profile.objects.create(
            user_id=user.id,
            lockId=create_lock()
        )
    return username, password


class GetCreateUpdateUsrsTestCase(TestCase):
    """Тесты на создание, добавление номера через форму"""

    def setUp(self):
        self.client = Client()
        s = self.client.get("/login/")
        self.csrftoken = s.cookies["csrftoken"].value

    def test_login_logout(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/login/", {
            "username": "anonim",
            "password": "wrong",
            "csrfmiddlewaretoken": self.csrftoken

        })

        self.assertNotIn("sessionid", response.cookies, response.status_code)

        username, password = create_profile(False)

        response = self.client.post("/login/", {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": self.csrftoken
        })

        self.assertIn("sessionid", response.cookies, response.content)

        response = self.client.post("/logout/", {
            "csrfmiddlewaretoken": self.csrftoken
        })

        self.assertNotIn("sessionid", response.cookies, response.status_code)

