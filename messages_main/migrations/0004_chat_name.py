# Generated by Django 5.0.4 on 2024-06-18 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0003_message_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name'),
        ),
    ]
