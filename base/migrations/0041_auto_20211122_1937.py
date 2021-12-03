# Generated by Django 3.2.9 on 2021-11-22 19:37

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0040_alter_power_range'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='power',
            name='effect',
        ),
        migrations.RemoveField(
            model_name='power',
            name='hit_effect',
        ),
        migrations.RemoveField(
            model_name='power',
            name='miss_effect',
        ),
        migrations.RemoveField(
            model_name='power',
            name='requirement',
        ),
        migrations.RemoveField(
            model_name='power',
            name='target',
        ),
        migrations.RemoveField(
            model_name='power',
            name='trigger',
        ),
        migrations.AlterField(
            model_name='power',
            name='effect_type',
            field=multiselectfield.db.fields.MultiSelectField(
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
                default='NONE',
                max_length=113,
                verbose_name='Тип эффекта',
            ),
        ),
        migrations.DeleteModel(
            name='PowerTarget',
        ),
    ]