import requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, EventForm, RegistrationForm
from rest_framework import generics
from .models import Event, User
from .serializers import EventSerializer, UserSerializer
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django import forms
from django.db import models
from django import forms
from .models import Event
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.decorators import login_required

def start(request):
    return render(request, 'start.html')

def enter(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['login']
            password = form.cleaned_data['password']

            data = {'login': login_input, 'password': password}
            headers = {'X-Request-Source': 'web', 'Accept': 'application/json'}

            try:
                response = requests.post('http://37.9.4.22:8080/api/auth/sign-in', json=data, headers=headers)

                if response.status_code == 400:
                    messages.error(request, 'Неверный логин или пароль.')
                else:
                    response.raise_for_status()
                    token = response.text.strip()
                    if token:
                        request.session['auth_token'] = token

                        user_info_response = requests.get('http://37.9.4.22:8080/api/users', headers={
                            'Authorization': f"Bearer Bearer {token}",
                            'Accept': 'application/json'
                        })

                        user_data = {}
                        if user_info_response.status_code == 200:
                            user_data = user_info_response.json()
                            request.session['user_data'] = user_data

                        login_name = user_data.get('login') or login_input
                        user, created = User.objects.get_or_create(username=login_name)

                        if created:
                            user.set_unusable_password()
                            user.save()

                        django_login(request, user)
                        messages.success(request, 'Вы успешно вошли в систему!')
                        return redirect('profile')
                    else:
                        messages.error(request, 'Не удалось получить токен авторизации.')

            except requests.exceptions.RequestException as e:
                pass  # messages.error(request, f'Ошибка сети: {e}')
            except ValueError as e:
                pass  # messages.error(request, f'Ошибка разбора ответа: {e}')

    return render(request, 'enter.html', {'form': form})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user  # Привязываем событие к текущему пользователю
            event.save()
            return redirect('profile')  # После создания события перенаправляем в профиль
    else:
        form = EventForm()

    return render(request, 'forma.html', {'form': form})




@login_required(login_url=None)
def profile(request):
    token = request.session.get('access_token')

    try:
        user_data = request.session.get('user_data', {})
    except Exception:
        user_data = {}

    user_data['name'] = user_data.get('name', 'Неизвестно')
    user_data['username'] = user_data.get('username', 'Неизвестно')
    user_data['email'] = user_data.get('email', 'Неизвестно')
    user_data['phone'] = user_data.get('phone', 'Неизвестно')

    user_data = request.session.get('user_data', {})
    events = Event.objects.filter(creator=request.user)
    return render(request, 'profile.html', {
        'user_data': user_data,
        'events': events
    })



@login_required(login_url=None)
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


@login_required(login_url=None)
def edit_event(request, event_id):
    user = request.user
    event = get_object_or_404(Event, id=event_id, creator=user)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {
        'form': form,
        'event': event,
    })



@login_required(login_url=None)
def delete_event(request, event_id):
    token = request.session.get('access_token')
    headers = {
        'Authorization': f'Bearer Bearer {token}',
        'X-Request-Source': 'web',
    } if token else {}

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        try:
            requests.delete(f'http://37.9.4.22:8080/api/creator/events/{event_id}', headers=headers)
        except requests.exceptions.RequestException:
            pass  # можно закомментировать сообщения об ошибках

        event.delete()  # удаление из локальной базы
        return redirect('profile')

    return render(request, 'delete_event.html', {'event': event})



def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("fkjuhg")
        if form.is_valid():
            registration_data = form.cleaned_data
            print("fkjuhg")
            try:
                response = requests.post('http://37.9.4.22:8080/api/auth/sign-up', json=registration_data)

                if response.status_code == 400:
                    messages.error(request, 'Ошибка регистрации. Возможно, такой пользователь уже существует.')
                else:
                    response.raise_for_status()
                    return redirect('enter')

            except requests.exceptions.RequestException as e:
                messages.error(request, f'Ошибка регистрации: {e}')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


    return render(request, 'registration.html', {'form': form})




def custom_login_redirect(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Вы должны быть авторизованы, чтобы просматривать эту страницу.')
    return redirect('profile')

class CustomLogoutView(LogoutView):
    def get_next_page(self):
        return reverse('enter')


