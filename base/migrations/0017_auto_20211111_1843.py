# Generated by Django 3.2.9 on 2021-11-11 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_weapontype_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weapontype',
            name='category',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='damage_dice',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='dice_number',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='group',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='handedness',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='prof_bonus',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='properties',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='range',
        ),
    ]
