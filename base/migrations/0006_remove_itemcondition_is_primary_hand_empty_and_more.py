# Generated by Django 5.1.4 on 2024-12-18 14:47

import django.db.models.deletion
import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_itemcondition_is_primary_hand_empty_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemcondition',
            name='is_primary_hand_empty',
        ),
        migrations.RemoveField(
            model_name='itemcondition',
            name='is_secondary_hand_empty',
        ),
        migrations.RemoveField(
            model_name='itemcondition',
            name='primary_hand_category',
        ),
        migrations.RemoveField(
            model_name='itemcondition',
            name='primary_hand_group',
        ),
        migrations.RemoveField(
            model_name='itemcondition',
            name='primary_hand_type',
        ),
        migrations.RemoveField(
            model_name='itemcondition',
            name='secondary_hand_category',
        ),
        migrations.RemoveField(
            model_name='itemcondition',
            name='secondary_hand_group',
        ),
        migrations.RemoveField(
            model_name='itemcondition',
            name='secondary_hand_type',
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='group',
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ('CROSSBOW', 'Арбалет'),
                    ('UNARMED', 'Безоружное'),
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
                max_length=97,
                verbose_name='Group',
            ),
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='handedness',
            field=models.CharField(
                choices=[
                    ('ONE', 'Одноручное'),
                    ('TWO', 'Двуручное'),
                    ('VERSATILE', 'Универсальное'),
                    ('FREE', 'Не занимает руки'),
                    ('DOUBLE', 'Двойное'),
                ],
                max_length=9,
                verbose_name='Handedness',
            ),
        ),
        migrations.CreateModel(
            name='WeaponState',
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
                (
                    'is_empty',
                    models.BooleanField(
                        default=False, verbose_name='Is primary hand empty'
                    ),
                ),
                ('is_off_hand', models.BooleanField(default=False)),
                ('is_reach', models.BooleanField(default=False)),
                (
                    'category',
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[
                            (1, 'Простое рукопашное'),
                            (2, 'Воинское рукопашное'),
                            (3, 'Превосходное рукопашное'),
                            (4, 'Простое дальнобойное'),
                            (5, 'Воинское дальнобойное'),
                            (6, 'Превосходное дальнобойное'),
                            (7, 'Инструмент'),
                        ],
                        max_length=13,
                        null=True,
                        verbose_name='Primary hand category',
                    ),
                ),
                (
                    'group',
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[
                            ('CROSSBOW', 'Арбалет'),
                            ('UNARMED', 'Безоружное'),
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
                        max_length=97,
                        null=True,
                        verbose_name='Primary hand group',
                    ),
                ),
                (
                    'type',
                    models.ManyToManyField(
                        blank=True,
                        related_name='primary_hand_conditions',
                        to='base.weapontype',
                        verbose_name='Primary hand',
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='itemcondition',
            name='primary_hand',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='primary_hands',
                to='base.weaponstate',
            ),
        ),
        migrations.AddField(
            model_name='itemcondition',
            name='secondary_hand',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='secondary_hands',
                to='base.weaponstate',
            ),
        ),
    ]
