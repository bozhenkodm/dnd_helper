# Generated by Django 3.2.9 on 2021-11-24 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0051_auto_20211124_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='encounter',
            name='roll_for_players',
            field=models.BooleanField(
                default=False, verbose_name='Кидать инициативу за игроков?'
            ),
        ),
        migrations.AlterField(
            model_name='combatants',
            name='encounter',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='combatants',
                to='base.encounter',
                verbose_name='Сцена',
            ),
        ),
    ]
