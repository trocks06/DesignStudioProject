from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator, EmailValidator

from .models import AdvUser


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = AdvUser
        fields = ['username', 'password']

class UserRegisterForm(UserCreationForm):
    latin_validator = RegexValidator(
        regex=r'^[a-zA-Z-]*$',
        message='Имя пользователя может содержать только латинские буквы и дефис.',
    )
    kiril_validator = RegexValidator(
        regex=r'^[а-яА-Я- ]*$',
        message='ФИО может содержать только кириллицу, дефис и пробелы'
    )
    def clean_username(self):
        username = self.cleaned_data['username']
        if AdvUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким ником уже существует')
        return username

    agree_to_terms = forms.BooleanField(
        label='Я согласен с обработкой персональных данных',
        required=True,
    )

    def clean_agree_to_terms(self):
        if not self.cleaned_data['agree_to_terms']:
            raise forms.ValidationError('Требуется согласие на обработку персональных данных')
        return self.cleaned_data['agree_to_terms']

    username = forms.CharField(validators=[latin_validator])
    first_name = forms.CharField(validators=[kiril_validator])
    last_name = forms.CharField(validators=[kiril_validator])
    patronymic = forms.CharField(validators=[kiril_validator])
    email = forms.EmailField(validators=[EmailValidator()])

    class Meta:
        model = AdvUser
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email', 'password1', 'password2', 'agree_to_terms']