# Generated by Django 3.0.6 on 2020-06-17 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_transactions', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CreditTransaction',
        ),
        migrations.AlterField(
            model_name='debittransaction',
            name='summary',
            field=models.CharField(choices=[('send', 'send')], default='send', max_length=250),
        ),
        migrations.AlterField(
            model_name='debittransaction',
            name='type',
            field=models.CharField(choices=[('debit', 'debit')], default='debit', max_length=250),
        ),
    ]
