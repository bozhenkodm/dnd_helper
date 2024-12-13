# Generated by Django 5.1.4 on 2024-12-15 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='trained_skills',
            field=models.ManyToManyField(
                blank=True, to='base.skill', verbose_name='Trained skills'
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='var_bonus_ability',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='base.ability',
                verbose_name='Selective ability bonus',
            ),
        ),
    ]
