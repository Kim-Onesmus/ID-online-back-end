from django.forms import ModelForm, TextInput, Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, ConfirmationDocument
from django import forms


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class ConfirmationDocumentForm(forms.ModelForm):
    class Meta:
        model = ConfirmationDocument
        fields = '__all__'