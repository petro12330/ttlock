
from datetime import datetime


from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponseBadRequest, HttpResponse, Http404, \
    HttpResponseRedirect
import json

from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from .forms import PhoneForm, CreateUserForm
from . import models
from .services.lock_service import create_user

REDIRECT_FIELD_NAME = '/'


def send_message(user):
    print(f"Пришел ученик {user.username}, время прихода {user.lockDate}")


def check_in_base(data, request):
    ttlock = models.Ttlock.objects.get(
        profile__user=request.user
    )
    for user_data in data:
        username = user_data['username']
        # lockDate = user_data["lockDate"]
        lockDate = datetime.utcfromtimestamp(
            int(str(user_data["serverDate"])[:-3])).strftime(
            '%H:%M  %d.%m.%Y')
        keyboardPwd = user_data["keyboardPwd"]
        recordType = user_data["recordType"]
        success = user_data["success"],
        try:
            user = models.TtlockUser.objects.get(
                lockId=ttlock,
                keyboardPwd=keyboardPwd,
                username=username,
                success=1,
            )
            if user.lockDate < lockDate:
                user.lockDate = lockDate
                user.save()
                send_message(user)
        except Exception:
            try:
                user = models.TtlockUser.objects.create(
                    lockId=ttlock,
                    lockDate=lockDate,
                    recordType=recordType,
                    success=user_data["success"],
                    keyboardPwd=keyboardPwd,
                    username=username,
                )
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


@csrf_exempt
def update_or_auto_create_user(request):
    if request.method == 'POST':
        body = request.body
        data = json.loads(body)
        check_in_base(data, request)
        return HttpResponse("OK", status=201)
    return HttpResponse("Bad", status=404)


def list_users(request, error=None):
    phone_form = PhoneForm()
    if request.method == 'POST':
        if "create_user_btn" in request.POST:
            error = create_new_user(request)
            return HttpResponseRedirect("/")
        if "update_phone_btn" in request.POST:
            error = add_phone_user(request)
            return HttpResponseRedirect("/")
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect("/login/")
    users = models.TtlockUser.objects.filter(
        lockId__profile__user=user).order_by("-lockDate")
    phone_form = PhoneForm()
    create_user_form = CreateUserForm()
    return render(request, "ttlock/list.html", {"users": users,
                                                "phone_form": phone_form,
                                                "create_user_form": create_user_form,
                                                "error": error
                                                })


def redirerect_home(request):
    return HttpResponseRedirect("/")


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
