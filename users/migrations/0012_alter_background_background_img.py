# Generated by Django 5.0.4 on 2024-05-07 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_background_background_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='background',
            name='background_img',
            field=models.ImageField(default='4.png', max_length=10000, upload_to='backgrounds/% Y/% m/% d/'),
        ),
    ]
