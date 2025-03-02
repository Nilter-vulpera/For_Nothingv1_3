# Generated by Django 5.0.4 on 2024-06-23 17:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0007_message_read_message_read_timestamp_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='read',
        ),
        migrations.RemoveField(
            model_name='message',
            name='read_timestamp',
        ),
        migrations.CreateModel(
            name='MessageReadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('read_timestamp', models.DateTimeField(blank=True, null=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_statuses', to='messages_main.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_statuses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
