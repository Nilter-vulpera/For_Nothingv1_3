# Generated by Django 5.0.4 on 2025-02-26 11:59

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_friendshiprequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='background',
            name='background_img',
            field=models.ImageField(upload_to=users.models.user_directory_path),
        ),
    ]
