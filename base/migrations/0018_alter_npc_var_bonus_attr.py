# Generated by Django 4.0 on 2021-12-15 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_power_accessory_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='var_bonus_attr',
            field=models.CharField(
                choices=[
                    ('STRENGTH', 'Сила'),
                    ('CONSTITUTION', 'Телосложение'),
                    ('DEXTERITY', 'Ловкость'),
                    ('INTELLIGENCE', 'Интеллект'),
                    ('WISDOM', 'Мудрость'),
                    ('CHARISMA', 'Харизма'),
                ],
                max_length=12,
                null=True,
                verbose_name='Выборочный бонус характеристики',
            ),
        ),
    ]
