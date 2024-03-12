from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Photo, ConfirmationDocument

@receiver(pre_save, sender=Photo)
@receiver(pre_save, sender=ConfirmationDocument)
def send_status_update_email(sender, instance, **kwargs):
    # Check if the status field is changed
    if instance.pk:  # Check if the instance is already in the database
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.status != instance.status and instance.status == 'approved':
            subject = 'ID application status updates'
            message = 'Your ID application status has been updated. \nPlease log in to check the status of your application'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.client.email, ]
            send_mail(subject, message, email_from, recipient_list)




