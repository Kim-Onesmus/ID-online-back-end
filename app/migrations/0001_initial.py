# Generated by Django 5.0.1 on 2024-03-02 10:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('sender', models.CharField(max_length=100)),
                ('messange', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('sur_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('username', models.CharField(max_length=50)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('profile_picture', models.ImageField(blank=True, default='media/profile.png', null=True, upload_to='media')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BathNo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_no', models.PositiveIntegerField()),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='applyID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmationDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('birth_certificate', models.FileField(upload_to='media')),
                ('location_doc', models.FileField(upload_to='media')),
                ('parent_id', models.FileField(upload_to='media')),
                ('status', models.CharField(choices=[('approved', 'approved'), ('pending', 'pending'), ('cancelled', 'cancelled')], default='pending', max_length=200)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=1000)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='IDCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('serial_number', models.PositiveIntegerField(unique=True)),
                ('id_number', models.PositiveIntegerField(unique=True)),
                ('back_serial', models.CharField(max_length=12, unique=True)),
                ('random_number', models.CharField(max_length=200, unique=True)),
                ('principal_sign', models.ImageField(upload_to='')),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='LocatioDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('county', models.CharField(max_length=100)),
                ('sub_county', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('division', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('sub_location', models.CharField(max_length=100)),
                ('village', models.CharField(max_length=100)),
                ('land_mark', models.CharField(max_length=100)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='LostId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_time', models.TimeField(auto_now_add=True)),
                ('select', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=500)),
                ('status', models.CharField(choices=[('approved', 'approved'), ('pending', 'pending'), ('cancelled', 'cancelled')], default='pending', max_length=200)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='LostPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_time', models.TimeField(auto_now_add=True)),
                ('number', models.PositiveBigIntegerField(max_length=13)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_time', models.TimeField(auto_now_add=True)),
                ('number', models.PositiveBigIntegerField(max_length=13)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('approved', 'approved'), ('pending', 'pending'), ('cancelled', 'cancelled')], default='pending', max_length=200)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
    ]
