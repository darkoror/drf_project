# Generated by Django 2.2.19 on 2021-04-12 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_is_restoring_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_restoring_password',
        ),
    ]
