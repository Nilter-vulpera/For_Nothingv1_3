# Generated by Django 5.0.4 on 2025-03-16 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0024_alter_chat_options_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['type', 'message_in_chat__pub_date']},
        ),
    ]
