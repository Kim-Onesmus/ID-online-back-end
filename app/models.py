from django.db import models
from django.contrib.auth.models import User



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
    status = models.CharField(max_length=200, choices=status, default='pending')

