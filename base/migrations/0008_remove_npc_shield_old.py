# Generated by Django 4.0.2 on 2022-02-12 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_rename_shield_npc_shield_old_alter_npc_arms_slot_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npc',
            name='shield_old',
        ),
    ]
