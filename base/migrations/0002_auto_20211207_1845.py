# Generated by Django 3.2.9 on 2021-12-07 18:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='primary_hand',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='in_primary_hands',
                to='base.weapon',
                verbose_name='Основная рука',
            ),
        ),
        migrations.AddField(
            model_name='npc',
            name='secondary_hand',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='in_secondary_hands',
                to='base.weapon',
                verbose_name='Вторичная рука',
            ),
        ),
    ]
