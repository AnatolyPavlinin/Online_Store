from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    """Форма регистрации с подтверждением пароля"""

    confirm_password = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(),
        help_text='Повторите пароль для подтверждения.'
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                {'confirm_password': 'Пароли не совпадают'}
            )

        return cleaned_data

    def send_welcome_email(self, user):
        subject = 'Добро пожаловать!'
        message = f'''Здравствуйте, {user.email}!\n
        Спасибо за регистрацию на нашем сайте.\n
        Приятных покупок!'''

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Форма входа"""
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )