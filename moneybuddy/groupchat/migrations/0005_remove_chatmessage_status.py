# Generated by Django 3.0.10 on 2020-11-30 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupchat', '0004_auto_20201129_0217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='status',
        ),
    ]