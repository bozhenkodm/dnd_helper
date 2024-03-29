# Generated by Django 4.0.2 on 2022-02-15 14:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0012_npc_creation_step'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abilities',
            fields=[
                (
                    'title',
                    models.CharField(
                        choices=[
                            ('INTELLIGENCE', 'Интеллект'),
                            ('DEXTERITY', 'Ловкость'),
                            ('WISDOM', 'Мудрость'),
                            ('STRENGTH', 'Сила'),
                            ('CONSTITUTION', 'Телосложение'),
                            ('CHARISMA', 'Харизма'),
                        ],
                        max_length=12,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.SlugField(
                choices=[
                    ('invoker', 'Апостол'),
                    ('artificer', 'Артефактор'),
                    ('bard', 'Бард'),
                    ('vampire', 'Вампир'),
                    ('barbarian', 'Варвар'),
                    ('warlord', 'Военачальник'),
                    ('warpriest', 'Военный священник (жрец)'),
                    ('fighter', 'Воин'),
                    ('wizard', 'Волшебник'),
                    ('druid', 'Друид'),
                    ('priest', 'Жрец'),
                    ('seeker', 'Ловчий'),
                    ('avenger', 'Каратель'),
                    ('warlock', 'Колдун'),
                    ('swordmage', 'Мечник-маг'),
                    ('monk', 'Монах'),
                    ('paladin', 'Паладин'),
                    ('rogue', 'Плут'),
                    ('runepriest', 'Рунный жрец'),
                    ('ranger', 'Следопыт'),
                    ('ranger_melee', 'Следопыт (Рукопашник)'),
                    ('hexblade', 'Хексблэйд (колдун)'),
                    ('warden', 'Хранитель'),
                    ('sorcerer', 'Чародей'),
                    ('shaman', 'Шаман'),
                ],
                max_length=12,
            ),
        ),
    ]
