# Generated by Django 5.0.4 on 2024-09-15 08:10

import messages_main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0012_message_photoformessages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='photoForMessages',
            field=models.ImageField(blank=True, upload_to=messages_main.models.user_directory_path),
        ),
    ]
