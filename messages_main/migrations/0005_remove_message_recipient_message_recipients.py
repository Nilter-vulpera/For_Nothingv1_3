# Generated by Django 5.0.4 on 2024-06-19 06:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0004_chat_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='recipient',
        ),
        migrations.AddField(
            model_name='message',
            name='recipients',
            field=models.ManyToManyField(related_name='recipient', to=settings.AUTH_USER_MODEL),
        ),
    ]
