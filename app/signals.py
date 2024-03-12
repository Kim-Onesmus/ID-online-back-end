from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Photo, ConfirmationDocument

@receiver(pre_save, sender=Photo)
@receiver(pre_save, sender=ConfirmationDocument)
def send_status_update_email(sender, instance, **kwargs):
    # Check if the status or reason field is changed
    if instance.pk:  # Check if the instance is already in the database
        old_instance = sender.objects.get(pk=instance.pk)

        # Check if status or reason is changed
        if old_instance.status != instance.status or old_instance.reason != instance.reason:
            subject = 'ID application status updates'
            
            # Include the reasons in the email message
            if instance.reason:
                message = f'Your ID application status has been updated to {instance.status}.\nReason: {instance.reason}\nPlease log in to check the status of your application.'
            else:
                message = 'Your ID application status has been updatedto {instance.status}. \nPlease log in to check the status of your application.'
            
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.client.email, ]
            
            send_mail(subject, message, email_from, recipient_list)
