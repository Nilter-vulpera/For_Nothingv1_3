# Generated by Django 4.1 on 2024-03-17 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_background_background_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='background',
            name='background_img',
            field=models.ImageField(default='4.png', upload_to='backgrounds/'),
        ),
    ]
