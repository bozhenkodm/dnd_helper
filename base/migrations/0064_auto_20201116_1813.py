# Generated by Django 3.1.3 on 2020-11-16 18:13

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0063_auto_20201116_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weapontype',
            name='group',
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ('CROSSBOW', 'Арбалет'),
                    ('MACE', 'Булава'),
                    ('POLEARM', 'Древковое'),
                    ('PICK', 'Кирка'),
                    ('SPEAR', 'Копьё'),
                    ('BOW', 'Лук'),
                    ('LIGHT_BLADE', 'Лёгкий клинок'),
                    ('HAMMER', 'Молот'),
                    ('STAFF', 'Посох'),
                    ('SLING', 'Праща'),
                    ('AXE', 'Топор'),
                    ('HEAVY_BLADE', 'Тяжелый клинок'),
                    ('FLAIL', 'Цеп'),
                ],
                max_length=89,
                verbose_name='Группа оружия',
            ),
        ),
    ]
