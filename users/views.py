from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            form.send_welcome_email(user)

            login(request, user)
            return redirect('catalog:home')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    """Авторизация пользователя"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalog:home')
            else:
                form.add_error(None, 'Неверный email или пароль')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})
