# Generated by Django 3.0.6 on 2020-06-21 02:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('bitcoin_balance', models.DecimalField(decimal_places=8, default=0.0, max_digits=50)),
                ('local_currency_balance', models.DecimalField(decimal_places=3, default=0.0, max_digits=50)),
                ('vault_balance', models.DecimalField(decimal_places=8, default=0.0, max_digits=50)),
                ('vault_release_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('referral', models.EmailField(blank=True, max_length=250, null=True)),
                ('agent_status', models.CharField(default=None, max_length=400)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
