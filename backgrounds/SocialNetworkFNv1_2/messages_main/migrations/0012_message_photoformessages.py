# Generated by Django 5.0.4 on 2024-09-15 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0011_messagereadstatus_alter_readreceipt_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='photoForMessages',
            field=models.ImageField(blank=True, upload_to='media/messages/%USERNAME%'),
        ),
    ]
