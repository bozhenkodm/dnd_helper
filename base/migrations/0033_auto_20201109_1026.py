# Generated by Django 3.0.5 on 2020-11-09 10:26

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_race_vision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='var_bonus_attrs',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('STRENGTH', 'Сила'),
                    ('CONSTITUTION', 'Телосложение'),
                    ('DEXTERITY', 'Ловкость'),
                    ('INTELLIGENCE', 'Интеллект'),
                    ('WISDOM', 'Мудрость'),
                    ('CHARISMA', 'Харизма'),
                ],
                max_length=60,
                null=True,
                verbose_name='Выборочные бонусы характеристик',
            ),
        ),
    ]
