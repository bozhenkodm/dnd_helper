# Generated by Django 5.1.4 on 2024-12-23 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_rename_const_ability_bonus_new_race_const_ability_bonus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='var_ability_bonus',
        ),
    ]