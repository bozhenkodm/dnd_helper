# Generated by Django 3.2.9 on 2021-11-24 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0052_auto_20211124_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='npcs',
            field=models.ManyToManyField(
                blank=True, to='base.NPC', verbose_name='Мастерские персонажи'
            ),
        ),
    ]
