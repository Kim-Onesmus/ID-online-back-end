from django.contrib import admin
from . models import Client, Notification, applyID, LocatioDetails
# Register your models here.

@admin.register(Client)
class ClientTable(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'sur_name', 'last_name', 'email', 'username', 'gender', 'phone', 'profile_picture')


@admin.register(Notification)
class NotificationTable(admin.ModelAdmin):
    list_display = ('date', 'time', 'sender', 'messange')


@admin.register(applyID)
class applyIDTable(admin.ModelAdmin):
    list_display = ('client', 'first_name', 'middle_name', 'last_name', 'date_of_birth')
