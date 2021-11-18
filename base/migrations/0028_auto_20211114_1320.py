# Generated by Django 3.2.9 on 2021-11-14 13:20

import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_alter_implementtype_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='available_implement_types',
        ),
        migrations.AddField(
            model_name='class',
            name='available_implement_types',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ('wand', 'Волшебная палочка'),
                    ('LongSword', 'Длинный меч'),
                    ('rod', 'Жезл'),
                    ('Dagger', 'Кинжал'),
                    ('Quaterstaff', 'Посох'),
                    ('holy_symbol', 'Символ веры'),
                    ('sphere', 'Сфера'),
                    ('totem', 'Тотем'),
                    ('ki_focus', 'Фокусировка ци'),
                ],
                max_length=71,
                null=True,
                verbose_name='Доступные инструменты',
            ),
        ),
        migrations.AlterField(
            model_name='implement',
            name='slug',
            field=models.CharField(max_length=20, verbose_name='Тип инструмента'),
        ),
        migrations.DeleteModel(
            name='ImplementType',
        ),
    ]