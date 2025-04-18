# Generated by Django 5.0.4 on 2024-07-05 20:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0010_readreceipt_remove_messagereadstatus_message_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageReadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='readreceipt',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='readreceipt',
            name='message',
        ),
        migrations.RemoveField(
            model_name='readreceipt',
            name='user',
        ),
        migrations.RemoveIndex(
            model_name='message',
            name='messages_ma_pub_dat_283a4e_idx',
        ),
        migrations.RemoveIndex(
            model_name='message',
            name='messages_ma_author__5047a4_idx',
        ),
        migrations.AddField(
            model_name='message',
            name='is_readed',
            field=models.BooleanField(default=False, verbose_name='Прочитано'),
        ),
        migrations.AlterField(
            model_name='message',
            name='color',
            field=models.CharField(choices=[('red', 'red'), ('green', 'green'), ('blue', 'blue'), ('black', 'black')], max_length=6),
        ),
        migrations.AddField(
            model_name='messagereadstatus',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_statuses', to='messages_main.message'),
        ),
        migrations.AddField(
            model_name='messagereadstatus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ReadReceipt',
        ),
    ]
