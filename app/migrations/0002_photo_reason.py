# Generated by Django 5.0.1 on 2024-02-19 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='reason',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]