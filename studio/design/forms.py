from PIL import Image
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator, EmailValidator

from .models import AdvUser, Application


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

    def clean_email(self):
        email = self.cleaned_data['email']
        if AdvUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже существует')
        return email

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
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email', 'password1', 'password2', 'agree_to_terms', 'is_employer']

class UserEditForm(UserChangeForm):
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
            raise forms.ValidationError('Данный ник занят')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if AdvUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Данная почта занята')
        return email

    username = forms.CharField(validators=[latin_validator])
    first_name = forms.CharField(validators=[kiril_validator])
    last_name = forms.CharField(validators=[kiril_validator])
    patronymic = forms.CharField(validators=[kiril_validator])
    email = forms.EmailField(validators=[EmailValidator()])
    class Meta:
        model = AdvUser
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email']

class ApplicationCreateForm(forms.ModelForm):
    def clean_app_image(self):
        app_image = self.cleaned_data.get('app_image')
        format_validator = ['JPEG', 'JPG', 'PNG', 'BMP']
        max_size = 2 * 1024 * 1024
        if app_image:
            if app_image.size > max_size:
                raise forms.ValidationError('Файл не должен весить более 2 мб')
            try:
                img = Image.open(app_image)
                img_format = img.format
                if img_format.upper() not in format_validator:
                    raise forms.ValidationError('Неверный формат файла. Допустимые форматы: JPEG, JPG, PNG, BMP.')
            except Exception:
                raise forms.ValidationError('Не удалось открыть файл как изображение')
        return app_image

    class Meta:
        model = Application
        fields = ['app_name', 'app_description', 'app_category', 'app_image']

class ApplicationEditForm(forms.ModelForm):
    def clean_app_image(self):
        design_image = self.cleaned_data.get('design_image')
        format_validator = ['JPEG', 'JPG', 'PNG', 'BMP']
        if design_image:
            try:
                img = Image.open(design_image)
                img_format = img.format
                if img_format.upper() not in format_validator:
                    raise forms.ValidationError('Неверный формат файла. Допустимые форматы: JPEG, JPG, PNG, BMP.')
            except Exception:
                raise forms.ValidationError('Не удалось открыть файл как изображение')
        return design_image

    class Meta:
        model = Application
        fields = ['design_image']