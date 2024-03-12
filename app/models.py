import random
import string

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import transaction



status = [
    ('approved','approved'),
    ('pending','pending'),
    ('cancelled','cancelled'),
]
# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    sur_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='media', default='media/profile.png')

class Notification(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sender = models.CharField(max_length=100)
    messange = models.CharField(max_length=1000)

class BathNo(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    birth_no = models.PositiveIntegerField()


class applyID(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()

class LocatioDetails(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    sub_location = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    land_mark = models.CharField(max_length=100)


class ConfirmationDocument(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    birth_certificate = models.FileField(upload_to='media')
    location_doc = models.FileField(upload_to='media')
    parent_id = models.FileField(upload_to='media')
    status = models.CharField(max_length=200, choices=status, default='pending')
    reason = models.CharField(max_length=200, blank=True, null=True)

class Photo(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=status, default='pending')
    reason = models.CharField(max_length=200, blank=True, null=True)


class IDCard(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    serial_number = models.PositiveIntegerField(unique=True)
    id_number = models.PositiveIntegerField(unique=True)
    back_serial = models.CharField(max_length=12, unique=True)
    random_number = models.CharField(max_length=200, unique=True)
    principal_sign = models.ImageField(default='sign.png', blank=True)

def generate_random_number(length):
    """Generate a random number of a specified length."""
    return ''.join(random.choices(string.digits, k=length))

def generate_back_serial(length):
    """Generate a random number of a specified length starting with 'T'."""
    return 'T' + ''.join(random.choices(string.digits, k=length-1))

def generate_unique_id_number():
    """Generate a unique ID number by incrementing a counter."""
    last_id_card = IDCard.objects.order_by('-id_number').first()
    if last_id_card:
        return last_id_card.id_number + 1
    else:
        return 38917851  # Initial value

@receiver(post_save, sender=IDCard)
def create_id_number(sender, instance, created, **kwargs):
    """Automatically generate and assign id_number when an IDCard is created or updated."""
    if created or not instance.id_number:
        instance.id_number = generate_unique_id_number()
        instance.save()


@receiver(post_save, sender=Photo)
@receiver(post_save, sender=ConfirmationDocument)
def create_id_card(sender, instance, **kwargs):
    # Check if both Photo and ConfirmationDocuments are approved
    photo_approved = Photo.objects.filter(client=instance.client, status='approved').exists()
    confirmation_docs_approved = ConfirmationDocument.objects.filter(client=instance.client, status='approved').exists()

    if photo_approved and confirmation_docs_approved:
        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Get or create the IDCard for the client
            id_card, created = IDCard.objects.get_or_create(
                client=instance.client,
                defaults={
                    'serial_number': random.randint(10**8, 10**9 - 1),
                    'back_serial': generate_back_serial(8),
                    'random_number': generate_random_number(30),
                    'id_number': generate_unique_id_number(),  # Generate id_number directly here
                }
            )



class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)

class Pay(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    number = models.PositiveBigIntegerField(max_length=13)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class LostId(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    select = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    file = models.FileField(upload_to='media')
    status = models.CharField(max_length=200, choices=status, default='pending')

class LostPay(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    number = models.PositiveBigIntegerField(max_length=13)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

