# Generated by Django 5.1.4 on 2024-12-23 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_remove_npc_var_bonus_ability'),
    ]

    operations = [
        migrations.RenameField(
            model_name='npc',
            old_name='var_bonus_ability_new',
            new_name='var_bonus_ability',
        ),
    ]
