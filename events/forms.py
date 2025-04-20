from django import forms
from .models import Event

class LoginForm(forms.Form):
    login = forms.CharField(max_length=150, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'attendee_count', 'image', 'moderation']


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=150, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    first_name = forms.CharField(max_length=150, label='Имя')
    last_name = forms.CharField(max_length=150, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Телефон')