# Generated by Django 3.0.6 on 2020-11-07 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0011_auto_20201107_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='referral_code',
            field=models.CharField(default='w', max_length=250),
        ),
    ]
