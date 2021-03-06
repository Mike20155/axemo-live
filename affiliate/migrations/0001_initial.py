# Generated by Django 3.0.6 on 2020-06-23 23:21

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
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('referral_code', models.CharField(default='teuvrvxohp', max_length=250)),
                ('referral_link', models.CharField(default='http://127.0.0.1:8000/home/register/rwdgydfjua', max_length=250)),
                ('fee_paid', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('agent_level', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('rank', models.CharField(choices=[('standard', 'standard'), ('pro', 'pro'), ('premium', 'premium')], default='standard', max_length=250)),
                ('primary_down_lines', models.TextField(default={})),
                ('secondary_down_lines', models.TextField(default={})),
                ('total_down_lines', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('total_earned', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
