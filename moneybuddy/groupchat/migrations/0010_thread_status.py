# Generated by Django 3.1.4 on 2020-12-20 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupchat', '0009_auto_20201220_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('N', 'Not Active')], default='N', max_length=1),
        ),
    ]
