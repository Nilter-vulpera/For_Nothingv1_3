# Generated by Django 4.1 on 2024-03-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='background',
            name='background_img',
            field=models.ImageField(default='2019-05-19_2.png', upload_to='backgrounds/'),
        ),
    ]
