from audioop import reverse
from datetime import datetime
from pprint import pprint

from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseBadRequest, HttpResponse, Http404, \
    HttpResponseRedirect
import json

from django.shortcuts import render
from . import models
from .forms import PhoneForm, CreateUserForm
from . import models
from .services.lock_service import create_user


def send_message(user):
    print(f"Пришел ученик {user.username}, время прихода {user.lockDate}")


def check_in_base(data):
    for user_data in data:
        lockDate = datetime.utcfromtimestamp(int(1627124350)).strftime(
            '%H:%M  %d.%m.%Y')
        try:
            user = models.TtlockUser.objects.get(
                lockId=user_data["lockId"],
                keyboardPwd=user_data["keyboardPwd"],
                username=user_data["username"],
            )
            if user.lockDate != lockDate:
                user.lockDate = lockDate
                user.save()
                send_message(user)
        except Exception:
            try:
                user = models.models.TtlockUser.objects.create(
                    lockId=user_data["lockId"],
                    lockDate=lockDate,
                    recordType=user_data["recordType"],
                    success=user_data["success"],
                    keyboardPwd=user_data["keyboardPwd"],
                    username=user_data["username"],
                )
                print("Новый ученик")
                send_message(user)
            except Exception:
                raise HttpResponseBadRequest


def get_data(body):
    try:
        list_with_values = ['lockId',
                            'serverDate',
                            'hotelUsername',
                            'recordType',
                            'success',
                            'keyboardPwd',
                            'username',
                            'lockDate']
        json_data = json.loads(body)
        for i in json_data:
            if i not in list_with_values:
                raise HttpResponseBadRequest
        return json_data
    except Exception:
        raise HttpResponseBadRequest


def update_or_auto_create_user(request):
    if request.method == 'POST':
        body = request.body
        data = json.loads(body)
        check_in_base(data)
        return HttpResponse("OK", status=201)
    return HttpResponse("Bad", status=404)


def list_users(request, error=None):
    if request.method == 'POST':
        if "create_user_btn" in request.POST:
            error = create_new_user(request)
        if "update_phone_btn" in request.POST:
            error = add_phone_user(request)
    print(request.user.is_authenticated())
    if not request.user.is_authenticated():
        HttpResponseRedirect("/login/")
    user=request.user
    users = models.TtlockUser.objects.filter(lockId__profile__user=user).order_by("-lockDate")
    phone_form = PhoneForm()
    create_user_form = CreateUserForm()
    return render(request, "ttlock/list.html", {"users": users,
                                                "phone_form": phone_form,
                                                "create_user_form":create_user_form,
                                                "error":error
                                                })


def add_phone_user(request):
    error = None
    form = PhoneForm(request.POST)
    if form.is_valid():
        try:
            user = models.TtlockUser.objects.get(id=request.POST['user_id'])
            user.phone = form.cleaned_data['phone']
            user.save()
            error = "Номер успешно добавлен"
            return error
        except Exception:
            raise Http404("Ученик не найден")
    error = "Номер должен начинаться с 7 и состоять из 11 цифр"
    return error

def create_new_user(request):
    error = None
    form = CreateUserForm(request.POST)
    if form.is_valid():
        ttlock = models.Ttlock.objects.get(
            profile__user=request.user
        )
        username = form.cleaned_data['username']
        phone = form.cleaned_data['phone']
        password = form.cleaned_data['password']
        if not create_user(ttlock.clientId, ttlock.access_token,
                           ttlock.client_secret, username, password):
            error = "Ошибка при создании пользователя"

        else:
            models.TtlockUser.objects.create(
                lockId=ttlock,
                phone=phone,
                keyboardPwd=password,
                username=username,
            )
            error = "Ученик успешно создан"
            return error
    else:
        error = "Пользовательно не создан, проверьте правильность данных"
    return error


class LogInView(LoginView):
    template_name = "login.html"

class LogOutView(LogoutView):
    template_name = ""