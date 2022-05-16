from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=40, label="Имя")
    password = forms.CharField(max_length=40, label="Имя")
    phone = forms.CharField(max_length=11, label="Телефон")

    def clean_phone(self):
        data = self.cleaned_data['phone']

        if len(data) != 11:
            raise ValidationError(_('Проверьте номер'))
        if int(data[0]) != 7:
            raise ValidationError(_('Проверьте номер'))
        int(self.cleaned_data['phone'])
        return data


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=11, label="Телефон")

    def clean_phone(self):
        data = self.cleaned_data['phone']

        if len(data) != 11:
            raise ValidationError(_('Проверьте номер'))
        if int(data[0]) != 7:
            raise ValidationError(_('Проверьте номер'))
        int(self.cleaned_data['phone'])
        return data
