from django.contrib import admin
from . models import Client
# Register your models here.

@admin.register(Client)
class ClientTable(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'sur_name', 'last_name', 'email', 'username', 'gender', 'phone', 'date_of_birth', 'profile_picture')