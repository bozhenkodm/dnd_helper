# Generated by Django 4.0 on 2021-12-17 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0002_encountericons'),
    ]

    operations = [
        migrations.AddField(
            model_name='encountericons',
            name='number_position',
            field=models.CharField(
                choices=[
                    ('BOTTOM_LEFT', 'bottom-left'),
                    ('BOTTOM_RIGHT', 'bottom-right'),
                    ('CENTER', 'center'),
                    ('TOP_LEFT', 'top-left'),
                    ('TOP_RIGHT', 'top-right'),
                ],
                default='TOP_LEFT',
                max_length=12,
                verbose_name='Класс позиции номера на картинке',
            ),
        ),
        migrations.AddField(
            model_name='encountericons',
            name='width',
            field=models.PositiveSmallIntegerField(default=200, verbose_name='Ширина'),
        ),
        migrations.AlterField(
            model_name='encountericons',
            name='base_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='encounter_icons',
                verbose_name='базовая картинка',
            ),
        ),
        migrations.AlterField(
            model_name='encountericons',
            name='number_color',
            field=models.CharField(
                choices=[('BLACK', 'Black'), ('RED', 'Red'), ('WHITE', 'White')],
                default='red',
                max_length=5,
                verbose_name='Цвет номера',
            ),
        ),
    ]
