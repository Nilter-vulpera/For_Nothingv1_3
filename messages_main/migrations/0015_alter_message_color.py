# Generated by Django 5.0.4 on 2024-12-18 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0014_alter_message_photoformessages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='color',
            field=models.CharField(choices=[('red', 'red'), ('green', 'green'), ('blue', 'blue'), ('black', 'black')], default='#f9f9f9', max_length=6),
        ),
    ]
