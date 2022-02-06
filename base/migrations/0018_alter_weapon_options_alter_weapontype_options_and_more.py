# Generated by Django 4.0.2 on 2022-02-04 11:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_armor_bonus_armor_class'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weapon',
            options={'verbose_name': 'Weapon', 'verbose_name_plural': 'Weapon'},
        ),
        migrations.AlterModelOptions(
            name='weapontype',
            options={
                'verbose_name': 'Weapon type',
                'verbose_name_plural': 'Weapon types',
            },
        ),
        migrations.AlterField(
            model_name='armor',
            name='armor_type',
            field=models.SmallIntegerField(
                choices=[
                    (0, 'Тканевый'),
                    (2, 'Кожаный'),
                    (3, 'Шкурный'),
                    (6, 'Кольчуга'),
                    (7, 'Чешуйчатый'),
                    (8, 'Латный'),
                ],
                verbose_name='Armor type',
            ),
        ),
        migrations.AlterField(
            model_name='armor',
            name='bonus_armor_class',
            field=models.SmallIntegerField(
                default=0,
                help_text='For high level magic armor',
                verbose_name='Additional armor class',
            ),
        ),
        migrations.AlterField(
            model_name='armor',
            name='skill_penalty',
            field=models.SmallIntegerField(default=0, verbose_name='Skills penalty'),
        ),
        migrations.AlterField(
            model_name='armor',
            name='speed_penalty',
            field=models.SmallIntegerField(default=0, verbose_name='Speed penalty'),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='weapon_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='base.weapontype',
                verbose_name='Weapon type',
            ),
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Title'),
        ),
    ]