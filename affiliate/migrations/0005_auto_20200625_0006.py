# Generated by Django 3.0.6 on 2020-06-24 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0004_auto_20200624_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='referral_link',
        ),
        migrations.AlterField(
            model_name='agent',
            name='referral_code',
            field=models.CharField(default='qzscfoftua', max_length=250),
        ),
    ]
