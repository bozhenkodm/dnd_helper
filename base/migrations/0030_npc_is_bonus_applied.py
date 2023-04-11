# Generated by Django 4.0.4 on 2022-05-02 10:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0029_encounter_is_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='is_bonus_applied',
            field=models.BooleanField(
                default=False,
                help_text='Бонус за уровень уменьшает количество исцелений',
                verbose_name='Применять бонус за уровень?',
            ),
        ),
    ]