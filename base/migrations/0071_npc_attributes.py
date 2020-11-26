# Generated by Django 3.1.3 on 2020-11-17 09:52

import re

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0070_auto_20201117_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='attributes',
            field=models.CharField(
                default='0,0,0,0,0,0',
                max_length=20,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile('^\\d+(?:,\\d+)*\\Z'),
                        code='invalid',
                        message='Enter only digits separated by commas.',
                    )
                ],
                verbose_name='Характеристики',
            ),
        ),
    ]
