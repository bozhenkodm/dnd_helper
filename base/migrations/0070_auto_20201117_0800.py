# Generated by Django 3.1.3 on 2020-11-17 08:00

import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0069_implement_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='implement_attack_attributes',
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
                verbose_name='Атакующие характеристики (инструмент)',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='implements',
            field=models.ManyToManyField(
                blank=True, to='base.Implement', verbose_name='Инструменты'
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='weapon_attack_attributes',
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ('STRENGTH', 'Сила'),
                    ('CONSTITUTION', 'Телосложение'),
                    ('DEXTERITY', 'Ловкость'),
                    ('INTELLIGENCE', 'Интеллект'),
                    ('WISDOM', 'Мудрость'),
                    ('CHARISMA', 'Харизма'),
                ],
                default='STRENGTH',
                max_length=60,
                verbose_name='Атакующие характеристики (оружие)',
            ),
        ),
    ]
