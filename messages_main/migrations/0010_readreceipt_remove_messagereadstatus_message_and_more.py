# Generated by Django 5.0.4 on 2024-07-04 17:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_main', '0009_rename_read_messagereadstatus_is_read_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('read_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='messagereadstatus',
            name='message',
        ),
        migrations.RemoveField(
            model_name='messagereadstatus',
            name='user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='is_readed',
        ),
        migrations.AlterField(
            model_name='message',
            name='color',
            field=models.CharField(choices=[('red', 'Red'), ('green', 'Green'), ('blue', 'Blue'), ('black', 'Black')], max_length=6),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['pub_date'], name='messages_ma_pub_dat_283a4e_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['author'], name='messages_ma_author__5047a4_idx'),
        ),
        migrations.AddField(
            model_name='readreceipt',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_receipts', to='messages_main.message'),
        ),
        migrations.AddField(
            model_name='readreceipt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='MessageReadStatus',
        ),
        migrations.AlterUniqueTogether(
            name='readreceipt',
            unique_together={('message', 'user')},
        ),
    ]
