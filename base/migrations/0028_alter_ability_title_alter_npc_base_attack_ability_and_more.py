# Generated by Django 4.0.2 on 2022-02-16 21:36

import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0027_remove_npc_var_bonus_ability_old'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ability',
            name='title',
            field=models.CharField(
                choices=[
                    ('intelligence', 'Интеллект'),
                    ('dexterity', 'Ловкость'),
                    ('wisdom', 'Мудрость'),
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('charisma', 'Харизма'),
                ],
                max_length=12,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='base_attack_ability',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('dexterity', 'Ловкость'),
                    ('intelligence', 'Интеллект'),
                    ('wisdom', 'Мудрость'),
                    ('charisma', 'Харизма'),
                ],
                max_length=60,
                null=True,
                verbose_name='Атакующие характеристики',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='base_charisma',
            field=models.SmallIntegerField(
                default=10, verbose_name='Харизма (базовая)'
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='base_constitution',
            field=models.SmallIntegerField(
                default=10, verbose_name='Телосложение (базовое)'
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='base_dexterity',
            field=models.SmallIntegerField(
                default=10, verbose_name='Ловкость (базовая)'
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='base_intelligence',
            field=models.SmallIntegerField(
                default=10, verbose_name='Интеллект (базовый)'
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='base_strength',
            field=models.SmallIntegerField(default=10, verbose_name='Сила (базовая)'),
        ),
        migrations.AlterField(
            model_name='npc',
            name='base_wisdom',
            field=models.SmallIntegerField(
                default=10, verbose_name='Мудрость (базовая)'
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='level14_bonus_abilities',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('dexterity', 'Ловкость'),
                    ('intelligence', 'Интеллект'),
                    ('wisdom', 'Мудрость'),
                    ('charisma', 'Харизма'),
                ],
                max_length=60,
                null=True,
                verbose_name='Бонус характеристики на 14 уровне',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='level18_bonus_abilities',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('dexterity', 'Ловкость'),
                    ('intelligence', 'Интеллект'),
                    ('wisdom', 'Мудрость'),
                    ('charisma', 'Харизма'),
                ],
                max_length=60,
                null=True,
                verbose_name='Бонус характеристики на 18 уровне',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='level24_bonus_abilities',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('dexterity', 'Ловкость'),
                    ('intelligence', 'Интеллект'),
                    ('wisdom', 'Мудрость'),
                    ('charisma', 'Харизма'),
                ],
                max_length=60,
                null=True,
                verbose_name='Бонус характеристики на 24 уровне',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='level28_bonus_abilities',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('dexterity', 'Ловкость'),
                    ('intelligence', 'Интеллект'),
                    ('wisdom', 'Мудрость'),
                    ('charisma', 'Харизма'),
                ],
                max_length=60,
                null=True,
                verbose_name='Бонус характеристики на 28 уровне',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='level4_bonus_abilities',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('dexterity', 'Ловкость'),
                    ('intelligence', 'Интеллект'),
                    ('wisdom', 'Мудрость'),
                    ('charisma', 'Харизма'),
                ],
                max_length=60,
                null=True,
                verbose_name='Бонус характеристики на 4 уровне',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='level8_bonus_abilities',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('dexterity', 'Ловкость'),
                    ('intelligence', 'Интеллект'),
                    ('wisdom', 'Мудрость'),
                    ('charisma', 'Харизма'),
                ],
                max_length=60,
                null=True,
                verbose_name='Бонус характеристики на 8 уровне',
            ),
        ),
        migrations.AlterField(
            model_name='power',
            name='attack_ability',
            field=models.CharField(
                blank=True,
                choices=[
                    ('strength', 'Сила'),
                    ('constitution', 'Телосложение'),
                    ('dexterity', 'Ловкость'),
                    ('intelligence', 'Интеллект'),
                    ('wisdom', 'Мудрость'),
                    ('charisma', 'Харизма'),
                ],
                max_length=12,
                null=True,
                verbose_name='Attack ability',
            ),
        ),
    ]