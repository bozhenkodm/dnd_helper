# Generated by Django 5.1.4 on 2024-12-28 13:30

from django.db import migrations, models

import printer.constants


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0004_gridmap_cols_gridmap_rows'),
    ]

    operations = [
        migrations.AddField(
            model_name='gridmap',
            name='grid_color',
            field=models.CharField(
                choices=[('white', 'Белый'), ('red', 'Красный'), ('black', 'Чёрный')],
                default=printer.constants.ColorsStyle['WHITE'],
                max_length=5,
                verbose_name='Цвет грида',
            ),
        ),
    ]