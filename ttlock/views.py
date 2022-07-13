import time
import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, Http404, \
    HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from base_ttlock_utils.base_lock import TTLock
from . import models
from .forms import PhoneForm, CreateUserForm
from .models import Ttlock
from .services.base_utils import write_to_json, open_to_json
from .services.holihop_service import update_user_payment, get_ed_units, get_ed_units_students, send_message_teachers
from .services.send_bonus import add_points_user
from .services.ttlock_user_service import translate_username, auto_users
from .services.lock_service import create_user

import json

GROUP_JSON_FILE = "list_group.json"


def delete_user(request):
    try:
        models.TtlockUser.objects.get(id=request.POST["user_id"]).delete()

    except Exception:
        raise Http404("Ученик не найден")


@csrf_exempt
def update_or_auto_create_user(request):
    if request.method == "POST":
        body = request.body
        data = json.loads(body)
        auto_users(data, request)
        return HttpResponse("OK", status=201)
    return HttpResponse("Bad", status=404)


@csrf_exempt
def update_or_auto_create_user2(request):
    if request.method == "POST":
        body = request.body
        data = json.loads(body)
        auto_users(data, request)
        return HttpResponse("OK", status=201)
    return HttpResponse("Bad", status=404)


def list_users(request, error=None):
    if request.method == "POST":
        if "create_user_btn" in request.POST:
            error = create_new_user(request)
            if error is None:
                return HttpResponseRedirect("/")
        elif "update_phone_btn" in request.POST:
            error = add_phone_user(request)
            if error is None:
                return HttpResponseRedirect("/")
        elif "delete_phone_btn" in request.POST:
            error = delete_phone_user(request)
            if error is None:
                return HttpResponseRedirect("/")
        elif "delete_user_btn" in request.POST:

            error = delete_user(request)
            if error is None:
                return HttpResponseRedirect("/")

    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect("/login/")
    users_with_out_data = models.TtlockUser.objects.filter(lockDate=None,
                                                           lockId__profile__user=user)
    users_with_data = sorted(
        models.TtlockUser.objects.exclude(id__in=users_with_out_data).filter(
            lockId__profile__user=user),
        key=lambda x: time.strptime(x.lockDate, "%H:%M  %d.%m.%Y"),
        reverse=True)
    phone_form = PhoneForm()
    create_user_form = CreateUserForm()
    return render(request, "ttlock/list.html", {
        "users_with_out_data": users_with_out_data,
        "users_with_data": users_with_data,
        "phone_form": phone_form,
        "create_user_form": create_user_form,
        "error": error
    }
                  )


def redirect_home(request):
    from django import db
    db.connections.close_all()
    return HttpResponseRedirect("/")


def add_phone_user(request):
    error = None
    form = PhoneForm(request.POST)
    if form.is_valid():
        try:
            user = models.TtlockUser.objects.get(id=request.POST["user_id"])
            user.phone = form.cleaned_data["phone"]
            user.save()
            return error
        except Exception:
            raise "Ученик не найден"
    error = "Номер должен начинаться с 7 и состоять из 11 цифр"
    return error


def delete_phone_user(request):
    try:
        user = models.TtlockUser.objects.get(id=request.POST["user_id"])
        user.phone = None
        user.save()
        HttpResponseRedirect("/")
    except Exception:
        raise Http404("Ученик не найден")


def create_new_user(request):
    ru_alf = " абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    error = None
    form = CreateUserForm(request.POST)
    if form.is_valid():
        ttlock = models.Ttlock.objects.get(
            profile__user=request.user
        )
        username_ru = form.cleaned_data["username"]
        for sym in username_ru:
            if sym.lower() not in ru_alf:
                return "Имя должно быть только на русском языке"
        username_en = translate_username(username_ru)
        phone = form.cleaned_data["phone"]
        password = form.cleaned_data["password"]
        if create_user(ttlock.clientId, ttlock.access_token,
                       ttlock.client_secret, username_en, password):
            models.TtlockUser.objects.get_or_create(
                lockId=ttlock,
                phone=phone,
                keyboardPwd=password,
                username=username_ru,
            )
            return error

        else:
            error = "Ошибка при создании пользователя"
    else:
        error = "Пользовательно не создан, проверьте правильность данных"
    return error


@csrf_exempt
def create_points(request):
    body = json.loads(request.body)
    client_phone = body.get("client_phone")
    money = body.get("money")
    payment_method_id = body.get("payment_method_id", None)
    client_name = body.get("client_name")  # TODO для холихоп.
    error, status_code, text = add_points_user(money, client_phone)
    if error:
        return HttpResponse(content=error + text, status=status_code)
    error, status_code, text = update_user_payment(money, client_phone, payment_method_id)
    return HttpResponse(content=error + text, status=status_code)


@csrf_exempt
def open_door(request):
    body = json.loads(request.body)
    now = datetime.datetime.now()
    if 8 < now.hour <= 20:
        lock_id = body.get("lock_id")
        lock_obj = Ttlock.objects.get(lockId=lock_id)
        remote_lock = TTLock(clientId=lock_obj.clientId, accessToken=lock_obj.access_token)
        remote_lock.unlock(lockId=lock_id)
        return HttpResponse(content='ok', status=200)


@csrf_exempt
def write_list_notify_group(request):  # Делает рассылку по учителям/записывает группы в файл
    groups, teachers = get_ed_units()
    send_message_teachers(groups, teachers)
    # write_to_json(groups, GROUP_JSON_FILE) # TODO
    return HttpResponse(content='ok', status=200)


@csrf_exempt
def write_list_notify_students(request):  # Делает рассылку по ученикам/берет данные по группам из файла
    groups = open_to_json(GROUP_JSON_FILE)
    ed_units = get_ed_units_students(groups)
    print(ed_units)
    return HttpResponse(content='ok', status=200)


class LogInView(FormView):
    form_class = AuthenticationForm

    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LogInView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login")
