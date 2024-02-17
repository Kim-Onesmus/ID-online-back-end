# Generated by Django 5.0.1 on 2024-02-17 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='date_of_birth',
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
    ]
