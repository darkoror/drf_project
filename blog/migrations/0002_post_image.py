# Generated by Django 2.2.19 on 2021-05-06 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='posts_images'),
        ),
    ]