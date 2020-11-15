from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as login_auth
from . import forms
from utils.response_object import create_response_object


def login(request):
    """
    Метод аутентификации с полями username и password
    :param request: Объект запроса django, хранит в себе headers, data
    :return: http ответ с результатом аутентификации
    """
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            login_auth(request, form.user)
            return create_response_object(False, 'Успешно')
        else:
            return create_response_object(True, form.errors)


def acc_logout(request):
    """
    Метод выхода аккаунта из профиля, очищает сессию
    :param request: Объект запроса django, хранит в себе headers, data
    :return: переадресацию на главную страницу
    """
    logout(request)
    return redirect('/')


def login_page(request):
    """
    Метод отрисовки html страницы
    :param request: Объект запроса django, хранит в себе headers, data
    :return: переадресацию на главную страницу
    """
    if not request.user.is_authenticated:
        return render(request, 'authentication/sign.html')
    else:
        return redirect('/')


def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_auth(request, user)
                return create_response_object(False, 'OK')
            else:
                return create_response_object(True, 'Ошибка авторизации зарегистрированного пользователя')
        else:
            return create_response_object(True, form.errors)