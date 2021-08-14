from django.http import Http404

from ttlock import models
from ttlock.forms import PhoneForm


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
            raise Http404("Ученик не найден")
    error = "Номер должен начинаться с 7 и состоять из 11 цифр"
    return error