# Generated by Django 3.1.4 on 2020-12-25 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupchat', '0014_auto_20201226_0225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ('monthly_charge',)},
        ),
        migrations.RenameField(
            model_name='thread',
            old_name='total_buyout',
            new_name='monthly_charge',
        ),
    ]