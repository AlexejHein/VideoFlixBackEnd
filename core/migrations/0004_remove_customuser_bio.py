# Generated by Django 4.2.13 on 2024-07-14 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_customuser_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
    ]
