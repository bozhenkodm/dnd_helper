# Generated by Django 3.1.3 on 2021-02-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0049_auto_20210218_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='name',
            field=models.CharField(
                choices=[
                    ('BUGBEAR', 'Багбир'),
                    ('HAMADRYAD', 'Гамадриада'),
                    ('GITHZERAI', 'Гитзерай'),
                    ('GNOLL', 'Гнолл'),
                    ('GNOME', 'Гном'),
                    ('GOBLIN', 'Гоблин'),
                    ('GOLIATH', 'Голиаф'),
                    ('DWARF', 'Дварф'),
                    ('DEVA', 'Дев'),
                    ('GENASI_WINDSOUL', 'Дженази, ветер'),
                    ('GENASI_WATERSOUL', 'Дженази, вода'),
                    ('GENASI_EARTHSOUL', 'Дженази, земля'),
                    ('GENASI_FIRESOUL', 'Дженази, огонь'),
                    ('GENASI_STORMSOUL', 'Дженази, шторм'),
                    ('WILDEN', 'Дикарь'),
                    ('DOPPELGANGER', 'Доппельгангер'),
                    ('DRAGONBORN', 'Драконорожденный'),
                    ('TREANT', 'Древень'),
                    ('DROW', 'Дроу'),
                    ('DUERGAR', 'Дуэргар'),
                    ('KALASHTAR', 'Калаштар'),
                    ('KENKU', 'Кенку'),
                    ('KOBOLD', 'Кобольд'),
                    ('WARFORGED', 'Кованый'),
                    ('MINOTAUR', 'Минотавр'),
                    ('ORC', 'Орк'),
                    ('PIXIE', 'Пикси'),
                    ('HALFORC', 'Полуорк'),
                    ('HALFLING', 'Полурослик'),
                    ('HALFELF', 'Полуэльф'),
                    ('SATYR', 'Сатир'),
                    ('TIEFLING', 'Тифлинг'),
                    ('HOBGOBLIN', 'Хобгоблин'),
                    ('HUMAN', 'Человек'),
                    ('SHADAR_KAI', 'Шадар-Кай'),
                    ('SHIFTER_RAZORCLAW', 'Шифтер, бритволапый'),
                    ('SHIFTER_LONGTEETH', 'Шифтер, длиннозубый'),
                    ('ELADRIN', 'Эладрин'),
                    ('ELF', 'Эльф'),
                ],
                max_length=17,
                unique=True,
                verbose_name='Название',
            ),
        ),
    ]
