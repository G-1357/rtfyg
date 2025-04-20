from django import forms
from .models import Event

class LoginForm(forms.Form):
    login = forms.CharField(max_length=150, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'attendee_count', 'image', 'moderation']


