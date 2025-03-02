# Generated by Django 5.0.4 on 2024-07-03 11:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0008_remove_message_read_remove_message_read_timestamp_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagereadstatus',
            old_name='read',
            new_name='is_read',
        ),
        migrations.RenameField(
            model_name='messagereadstatus',
            old_name='read_timestamp',
            new_name='read_at',
        ),
        migrations.AlterField(
            model_name='messagereadstatus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
