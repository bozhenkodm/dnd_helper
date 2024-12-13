# Generated by Django 5.1.4 on 2024-12-18 14:52

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_itemcondition_armor_alter_itemcondition_shield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcondition',
            name='armor',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    (0, 'Тканевый'),
                    (2, 'Кожаный'),
                    (3, 'Шкурный'),
                    (6, 'Кольчуга'),
                    (7, 'Чешуйчатый'),
                    (8, 'Латный'),
                ],
                max_length=11,
                null=True,
                verbose_name='Armor type',
            ),
        ),
        migrations.AlterField(
            model_name='itemcondition',
            name='shield',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[(0, '----------'), (1, 'Лёгкий щит'), (2, 'Тяжелый щит')],
                max_length=5,
                null=True,
                verbose_name='Shield type',
            ),
        ),
    ]
