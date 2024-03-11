# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db import models

from .models import Photo, ConfirmationDocument

@receiver(post_save, sender=Photo)
@receiver(post_save, sender=ConfirmationDocument)
def send_status_update_email(sender, instance, **kwargs):
    # Check if the status field is changed
    if 'status' in instance.changed_fields() and instance.status == 'approved':
        subject = 'ID application status updates'
        message = 'Your ID application status has been updated. \nPlease log in to check the status of your application'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.client.email, ]
        send_mail(subject, message, email_from, recipient_list)
