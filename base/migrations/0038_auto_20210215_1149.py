# Generated by Django 3.1.3 on 2021-02-15 11:49

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0037_class_available_armor_types_int'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='available_armor_types_int',
        ),
        migrations.AlterField(
            model_name='class',
            name='available_armor_types',
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    (10, 'Тканевый'),
                    (20, 'Кожаный'),
                    (30, 'Шкурный'),
                    (40, 'Кольчуга'),
                    (50, 'Чешуйчатый'),
                    (60, 'Латный'),
                ],
                default=10,
                max_length=17,
                verbose_name='Ношение доспехов',
            ),
        ),
    ]
