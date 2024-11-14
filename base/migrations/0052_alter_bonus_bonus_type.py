# Generated by Django 5.1.2 on 2024-11-14 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0051_remove_race_bonus_race_bonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='bonus_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('ACROBATICS', 'Акробатика'),
                    ('ATTACK', 'Атака'),
                    ('ATHLETICS', 'Атлетика'),
                    ('PERCEPTION', 'Внимательность'),
                    ('WILL', 'Воля'),
                    ('THIEVERY', 'Воровство'),
                    ('ENDURANCE', 'Выносливость'),
                    ('INTIMIDATE', 'Запугивание'),
                    ('STREETWISE', 'Знание улиц'),
                    ('SURGE', 'Значение исцеления'),
                    ('INITIATIVE', 'Инициатива'),
                    ('INTELLIGENCE', 'Интеллект'),
                    ('HISTORY', 'История'),
                    ('ARMOR_CLASS', 'КД'),
                    ('SURGES', 'Количество исцелений'),
                    ('DEXTERITY', 'Ловкость'),
                    ('ARCANA', 'Магия'),
                    ('WISDOM', 'Мудрость'),
                    ('BLUFF', 'Обман'),
                    ('DIPLOMACY', 'Переговоры'),
                    ('DUNGEONEERING', 'Подземелья'),
                    ('NATURE', 'Природа'),
                    ('INSIGHT', 'Проницательность'),
                    ('REFLEX', 'Реакция'),
                    ('RELIGION', 'Религия'),
                    ('STRENGTH', 'Сила'),
                    ('SPEED', 'Скорость'),
                    ('STEALTH', 'Скрытность'),
                    ('FORTITUDE', 'Стойкость'),
                    ('CONSTITUTION', 'Телосложение'),
                    ('CHARISMA', 'Харизма'),
                    ('HEAL', 'Целительство'),
                ],
                max_length=13,
                null=True,
                verbose_name='Bonus type',
            ),
        ),
    ]
