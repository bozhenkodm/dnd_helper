# Generated by Django 4.0.2 on 2022-02-12 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_npc_shield_old'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='armsslotitem',
            unique_together={('magic_item_type', 'level', 'shield')},
        ),
    ]