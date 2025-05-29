from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
import uuid
from datetime import date
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input'}))
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'input'}),
        input_formats=['%d.%m.%Y']
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'birth_date', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удалим поле username (оно есть в UserCreationForm)
        self.fields.pop('username', None)

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 16:
            raise ValidationError("Регистрация доступна только пользователям от 16 лет.")

        return birth_date


    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = str(uuid.uuid4())  # Генерируем уникальный username
        if commit:
            user.save()
        return user
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"),widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'input'}))

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Аккаунт не активирован.", code='inactive')

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
