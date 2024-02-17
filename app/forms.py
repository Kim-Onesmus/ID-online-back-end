from django.forms import ModelForm, TextInput, Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client
from django import forms


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['email', 'username', 'phone', 'profile_picture']