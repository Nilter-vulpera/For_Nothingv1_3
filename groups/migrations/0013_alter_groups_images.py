# Generated by Django 5.0.4 on 2024-05-23 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0012_alter_groups_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='images',
            field=models.ImageField(default='/media/backgrounds/ForNothing.jpg', upload_to='media/GroupsImages'),
        ),
    ]
