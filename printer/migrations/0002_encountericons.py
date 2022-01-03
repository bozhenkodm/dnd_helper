# Generated by Django 4.0 on 2021-12-17 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncounterIcons',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=30, verbose_name='Название')),
                (
                    'base_image',
                    models.ImageField(
                        upload_to='encounter_icons', verbose_name='базовая картинка'
                    ),
                ),
                (
                    'number',
                    models.PositiveSmallIntegerField(
                        verbose_name='Количество однотипных'
                    ),
                ),
                (
                    'number_color',
                    models.CharField(
                        default='red', max_length=10, verbose_name='Цвет номера'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Иконка',
                'verbose_name_plural': 'Иконки',
            },
        ),
    ]