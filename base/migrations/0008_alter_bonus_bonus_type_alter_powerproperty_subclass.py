# Generated by Django 5.1.4 on 2024-12-28 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_bonus_bonus_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='bonus_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('STRENGTH', 'Сила'),
                    ('CONSTITUTION', 'Телосложение'),
                    ('DEXTERITY', 'Ловкость'),
                    ('INTELLIGENCE', 'Интеллект'),
                    ('WISDOM', 'Мудрость'),
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
                    ('ARMOR_CLASS', 'КД'),
                    ('FORTITUDE', 'Стойкость'),
                    ('REFLEX', 'Реакция'),
                    ('WILL', 'Воля'),
                    ('ATTACK', 'Атака'),
                    ('SURGE', 'Значение исцеления'),
                    ('INITIATIVE', 'Инициатива'),
                    ('POWER_SOURCE', 'Источник силы'),
                    ('SURGES', 'Количество исцелений'),
                    ('HIT_POINTS', 'Количество хитов'),
                    ('SIZE', 'Размер'),
                    ('ROLE', 'Роль'),
                    ('SPEED', 'Скорость'),
                    ('DAMAGE', 'Урон'),
                    ('SKILL_PENALTY', 'Штраф навыков'),
                    ('SPEED_PENALTY', 'Штраф скорости'),
                ],
                max_length=13,
                null=True,
                verbose_name='Bonus type',
            ),
        ),
        migrations.AlterField(
            model_name='powerproperty',
            name='subclass',
            field=models.SmallIntegerField(default=0, verbose_name='Subclass'),
        ),
    ]