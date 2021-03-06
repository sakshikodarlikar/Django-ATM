# Generated by Django 3.2.6 on 2021-10-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20211003_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bank_name',
            field=models.CharField(choices=[('axis', 'Axis Bank'), ('sbi', 'State Bank of India'), ('pnb', 'Punjab National Bank'), ('icici', 'ICICI Bank'), ('hdfc', 'HDFC Bank'), ('citi', 'Citi Bank'), ('indus', 'IndusInd Bank'), ('idbi', 'IDBI Bank'), ('bob', 'Bank of Baroda')], default='axis', max_length=100),
        ),
    ]
