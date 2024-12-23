# Generated by Django 5.1.4 on 2024-12-23 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_var_ability_bonus_new_race_var_ability_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='var_bonus_ability_new',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='base.abilitynew',
                verbose_name='Selective ability bonus',
            ),
        ),
    ]
