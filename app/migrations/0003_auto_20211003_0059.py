# Generated by Django 3.2.6 on 2021-10-02 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211003_0057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='id',
            new_name='account_id',
        ),
        migrations.RenameField(
            model_name='transfer',
            old_name='id',
            new_name='transfer_id',
        ),
    ]
