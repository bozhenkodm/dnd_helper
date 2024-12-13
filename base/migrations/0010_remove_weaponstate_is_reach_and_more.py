# Generated by Django 5.1.4 on 2024-12-19 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_bonus_item_condition_weapontype_distance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weaponstate',
            name='is_reach',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='is_reach',
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='distance',
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text='Additional distance for melee weapons, "reach".',
                verbose_name='Distance',
            ),
        ),
    ]
