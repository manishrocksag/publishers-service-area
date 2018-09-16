# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publisher_id', models.CharField(unique=True, max_length=254, verbose_name='user_id')),
                ('name', models.CharField(max_length=254, verbose_name='first name')),
                ('email', models.EmailField(max_length=70, unique=True, null=True, blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('language', models.IntegerField(default=0, choices=[(0, 'us_en'), (1, 'en')])),
                ('currency', models.IntegerField(default=0, choices=[(0, 'usd')])),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this publisher should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
            ],
            options={
                'verbose_name': 'publisher',
                'verbose_name_plural': 'publishers',
            },
        ),
    ]
