from django.contrib import admin
from . models import Client, Notification, applyID, LocatioDetails, ConfirmationDocument, Photo, Contact, Pay, LostId, LostPay, BathNo, IDCard
# Register your models here.,

@admin.register(Client)
class ClientTable(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'sur_name', 'last_name', 'email', 'username', 'gender', 'phone', 'profile_picture')


@admin.register(Notification)
class NotificationTable(admin.ModelAdmin):
    list_display = ('date', 'time', 'sender', 'messange')


@admin.register(BathNo)
class BathNoTable(admin.ModelAdmin):
    list_display = ('client', 'birth_no')

@admin.register(applyID)
class applyIDTable(admin.ModelAdmin):
    list_display = ('client', 'first_name', 'middle_name', 'last_name', 'date_of_birth')

@admin.register(LocatioDetails)
class LocatioDetailsTable(admin.ModelAdmin):
    list_display = ('client', 'date', 'county', 'sub_county', 'district', 'division', 'location', 'sub_location', 'village', 'land_mark')

@admin.register(ConfirmationDocument)
class ConfirmationDocumentTable(admin.ModelAdmin):
    list_display = ('client', 'birth_certificate', 'location_doc', 'parent_id', 'status')

@admin.register(Photo)
class PhotoTable(admin.ModelAdmin):
    list_display = ('client', 'image', 'status')

@admin.register(IDCard)
class IDcardTable(admin.ModelAdmin):
    list_display = ('client', 'serial_number', 'id_number', 'back_serial', 'random_number', 'date', 'time', 'principal_sign')

@admin.register(Contact)
class ContactTable(admin.ModelAdmin):
    list_display = ('client', 'name', 'email', 'subject', 'message', 'date', 'time')


@admin.register(Pay)
class PayTable(admin.ModelAdmin):
    list_display = ('client', 'created_date', 'created_time', 'number', 'amount')


@admin.register(LostId)
class LostIdTable(admin.ModelAdmin):
    list_display = ('client', 'created_date', 'created_time', 'select', 'text', 'status')

@admin.register(LostPay)
class LostPayTable(admin.ModelAdmin):
    list_display = ('client', 'created_date', 'created_time', 'number', 'amount')