# Generated by Django 3.0.5 on 2020-11-09 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_auto_20201109_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npc',
            name='hit_points_per_level',
        ),
        migrations.AddField(
            model_name='class',
            name='hit_points_per_level',
            field=models.PositiveSmallIntegerField(
                default=8, verbose_name='Хитов за уровень'
            ),
        ),
    ]
