# Generated by Django 5.1.4 on 2024-12-28 14:10

from django.db import migrations, models

import printer.constants


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0005_gridmap_grid_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encountericons',
            name='number_color',
            field=models.CharField(
                choices=[
                    ('white', 'Белый'),
                    ('green', 'Зелёный'),
                    ('red', 'Красный'),
                    ('black', 'Чёрный'),
                ],
                default=printer.constants.ColorsStyle['RED'],
                max_length=5,
                verbose_name='Цвет номера',
            ),
        ),
        migrations.AlterField(
            model_name='gridmap',
            name='grid_color',
            field=models.CharField(
                choices=[
                    ('white', 'Белый'),
                    ('green', 'Зелёный'),
                    ('red', 'Красный'),
                    ('black', 'Чёрный'),
                ],
                default=printer.constants.ColorsStyle['WHITE'],
                max_length=5,
                verbose_name='Цвет грида',
            ),
        ),
    ]
