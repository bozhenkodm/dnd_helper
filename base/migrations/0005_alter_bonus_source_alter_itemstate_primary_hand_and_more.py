# Generated by Django 5.1.4 on 2024-12-26 15:50

import django.db.models.deletion
import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_weaponstate_is_off_hand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='source',
            field=models.CharField(
                blank=True,
                choices=[
                    ('CLASS', 'Бонус класса'),
                    ('ITEM', 'Бонус предмета'),
                    ('POWER', 'Бонус таланта'),
                    ('FEAT', 'Бонус черты'),
                    ('SHIELD', 'Бонус щита'),
                    ('RACE', 'Расовый бонус'),
                ],
                max_length=6,
                null=True,
                verbose_name='Bonus source',
            ),
        ),
        migrations.AlterField(
            model_name='itemstate',
            name='primary_hand',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='primary_hands',
                to='base.weaponstate',
                verbose_name='Primary hand',
            ),
        ),
        migrations.AlterField(
            model_name='itemstate',
            name='secondary_hand',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='secondary_hands',
                to='base.weaponstate',
                verbose_name='Secondary hand',
            ),
        ),
        migrations.AlterField(
            model_name='itemstate',
            name='shield',
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[(1, 'Лёгкий щит'), (2, 'Тяжелый щит')],
                max_length=3,
                null=True,
                verbose_name='Shield type',
            ),
        ),
    ]