# Generated by Django 3.0.5 on 2020-11-08 16:28

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_npc_trained_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='trained_skills',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('ACROBATICS', 'Акробатика'),
                    ('ATHLETICS', 'Атлетика'),
                    ('INSIGHT', 'Внимательность'),
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
                    ('PERCEPTION', 'Проницательность'),
                    ('RELIGION', 'Религия'),
                    ('STEALTH', 'Скрытность'),
                    ('HEAL', 'Целительство'),
                ],
                max_length=154,
                null=True,
                verbose_name='Тренированные навыки',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='trained_skills',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('ACROBATICS', 'Акробатика'),
                    ('ATHLETICS', 'Атлетика'),
                    ('INSIGHT', 'Внимательность'),
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
                    ('PERCEPTION', 'Проницательность'),
                    ('RELIGION', 'Религия'),
                    ('STEALTH', 'Скрытность'),
                    ('HEAL', 'Целительство'),
                ],
                max_length=154,
                null=True,
                verbose_name='Тренированные навыки',
            ),
        ),
        migrations.AlterField(
            model_name='race',
            name='skill_bonuses',
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ('ACROBATICS', 'Акробатика'),
                    ('ATHLETICS', 'Атлетика'),
                    ('INSIGHT', 'Внимательность'),
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
                    ('PERCEPTION', 'Проницательность'),
                    ('RELIGION', 'Религия'),
                    ('STEALTH', 'Скрытность'),
                    ('HEAL', 'Целительство'),
                ],
                max_length=154,
                null=True,
                verbose_name='Бонусы навыков',
            ),
        ),
    ]
