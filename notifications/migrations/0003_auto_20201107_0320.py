# Generated by Django 3.0.6 on 2020-11-07 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20201107_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='data',
            field=models.CharField(max_length=5000000, null=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='data_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
