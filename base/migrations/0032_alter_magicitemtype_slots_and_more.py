# Generated by Django 4.1 on 2022-08-03 18:15

from django.db import migrations
from multiselectfield import MultiSelectField

import base.constants.constants


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0031_alter_npc_is_bonus_applied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magicitemtype',
            name='slots',
            field=MultiSelectField(
                choices=[
                    ('armor', 'Броня'),
                    ('head', 'Голова'),
                    ('ring', 'Кольца'),
                    ('feet', 'Обувь'),
                    ('weapon', 'Оружие'),
                    ('hands', 'Перчатки'),
                    ('waist', 'Пояс'),
                    ('arms', 'Предплечья/Щит'),
                    ('tatoo', 'Татуировка'),
                    ('wondrous_items', 'Чудесный предмет'),
                    ('neck', 'Шея'),
                ],
                max_length=70,
                null=True,
                verbose_name='Slots',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='base_attack_ability',
            field=MultiSelectField(
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
            name='level14_bonus_abilities',
            field=MultiSelectField(
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
            field=MultiSelectField(
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
            field=MultiSelectField(
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
            field=MultiSelectField(
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
            field=MultiSelectField(
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
            field=MultiSelectField(
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
            name='damage_type',
            field=MultiSelectField(
                choices=[
                    ('NONE', ''),
                    ('THUNDER', 'Звук'),
                    ('RADIANT', 'Излучение'),
                    ('ACID', 'Кислота'),
                    ('NECROTIC', 'Некротическая энергия'),
                    ('FIRE', 'Огонь'),
                    ('PSYCHIC', 'Психическая энергия'),
                    ('FORCE', 'Силовое поле'),
                    ('COLD', 'Холод'),
                    ('LIGHTNING', 'Электричество'),
                    ('POISON', 'Яд'),
                ],
                default=base.constants.constants.PowerDamageTypeEnum['NONE'],
                max_length=75,
                verbose_name='Damage type',
            ),
        ),
        migrations.AlterField(
            model_name='power',
            name='effect_type',
            field=MultiSelectField(
                choices=[
                    ('NONE', ''),
                    ('ZONE', 'Зона'),
                    ('CONJURATION', 'Иллюзия'),
                    ('HEALING', 'Исцеление'),
                    ('RELIABLE', 'Надежный'),
                    ('CHARM', 'Очарование'),
                    ('POLYMORPH', 'Превращение'),
                    ('SLEEP', 'Сон'),
                    ('STANCE', 'Стойка'),
                    ('FEAR', 'Страх'),
                    ('TELEPORTATION', 'Телепортация'),
                    ('RATTLING', 'Ужасающий'),
                    ('INVIGORATING', 'Укрепляющий'),
                    ('RAGE', 'Ярость'),
                ],
                default=base.constants.constants.PowerEffectTypeEnum['NONE'],
                max_length=113,
                verbose_name='Effect type',
            ),
        ),
    ]
