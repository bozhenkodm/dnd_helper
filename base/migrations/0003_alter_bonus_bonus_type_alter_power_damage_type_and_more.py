# Generated by Django 5.1.3 on 2024-12-04 22:16

import multiselectfield.db.fields
from django.db import migrations, models

import base.constants.constants


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_bonus_power_alter_power_action_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='bonus_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('INTELLIGENCE', 'Интеллект'),
                    ('DEXTERITY', 'Ловкость'),
                    ('WISDOM', 'Мудрость'),
                    ('STRENGTH', 'Сила'),
                    ('CONSTITUTION', 'Телосложение'),
                    ('CHARISMA', 'Харизма'),
                    ('ACROBATICS', 'Акробатика'),
                    ('ATHLETICS', 'Атлетика'),
                    ('PERCEPTION', 'Внимательность'),
                    ('THIEVERY', 'Воровство'),
                    ('ENDURANCE', 'Выносливость'),
                    ('INTIMIDATE', 'Запугивание'),
                    ('STREETWISE', 'Знание улиц'),
                    ('HISTORY', 'История'),
                    ('ARCANA', 'Магия'),
                    ('BLUFF', 'Обман'),
                    ('DIPLOMACY', 'Переговоры'),
                    ('DUNGEONEERING', 'Подземелья'),
                    ('NATURE', 'Природа'),
                    ('INSIGHT', 'Проницательность'),
                    ('RELIGION', 'Религия'),
                    ('STEALTH', 'Скрытность'),
                    ('HEAL', 'Целительство'),
                    ('WILL', 'Воля'),
                    ('ARMOR_CLASS', 'КД'),
                    ('REFLEX', 'Реакция'),
                    ('FORTITUDE', 'Стойкость'),
                    ('ATTACK', 'Атака'),
                    ('SURGE', 'Значение исцеления'),
                    ('INITIATIVE', 'Инициатива'),
                    ('SURGES', 'Количество исцелений'),
                    ('SPEED', 'Скорость'),
                    ('DAMAGE', 'Урон'),
                ],
                max_length=13,
                null=True,
                verbose_name='Bonus type',
            ),
        ),
        migrations.AlterField(
            model_name='power',
            name='damage_type',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
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
                null=True,
                verbose_name='Damage type',
            ),
        ),
        migrations.AlterField(
            model_name='power',
            name='effect_type',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
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
                null=True,
                verbose_name='Effect type',
            ),
        ),
    ]