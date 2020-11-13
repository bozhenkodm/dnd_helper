# Generated by Django 3.1.3 on 2020-11-13 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_auto_20201112_0757'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImplementType',
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
                ('name', models.CharField(max_length=20, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='WeaponType',
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
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                (
                    'prof_bonus',
                    models.SmallIntegerField(default=2, verbose_name='Бонус владения'),
                ),
                (
                    'group',
                    models.CharField(
                        choices=[
                            ('MACE', 'Булава'),
                            ('POLEARM', 'Древковое'),
                            ('PICK', 'Кирка'),
                            ('SPEAR', 'Копьё'),
                            ('LIGHT_BLADE', 'Лёгкий клинок'),
                            ('HAMMER', 'Молот'),
                            ('STAFF', 'Посох'),
                            ('AXE', 'Топор'),
                            ('HEAVY_BLADE', 'Тяжелый клинок'),
                            ('FLAIL', 'Цеп'),
                        ],
                        max_length=11,
                        verbose_name='Группа оружия',
                    ),
                ),
                (
                    'category',
                    models.CharField(
                        choices=[
                            ('MILITARY', 'Воинское'),
                            ('SUPERIOR', 'Превосходное'),
                            ('SIMPLE', 'Простое'),
                        ],
                        max_length=8,
                        verbose_name='Категория',
                    ),
                ),
                (
                    'damage',
                    models.CharField(
                        choices=[
                            ('D10', '1k10'),
                            ('D12', '1k12'),
                            ('D4', '1k4'),
                            ('D6', '1k6'),
                            ('D8', '1k8'),
                            ('D2_10', '2k10'),
                            ('D2_4', '2k4'),
                            ('D2_6', '2k6'),
                            ('D2_8', '2k8'),
                        ],
                        max_length=5,
                        verbose_name='',
                    ),
                ),
            ],
        ),
        migrations.RenameField(
            model_name='armor',
            old_name='type',
            new_name='armor_type',
        ),
        migrations.CreateModel(
            name='Weapon',
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
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                (
                    'enchantment',
                    models.SmallIntegerField(default=0, verbose_name='Улучшение'),
                ),
                (
                    'weapon_type',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='base.weapontype',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Implement',
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
                    'enchantment',
                    models.SmallIntegerField(default=0, verbose_name='Улучшение'),
                ),
                (
                    'implement_type',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='base.implementtype',
                    ),
                ),
            ],
        ),
    ]
