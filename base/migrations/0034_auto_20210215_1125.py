# Generated by Django 3.1.3 on 2021-02-15 11:25

from django.db import migrations

from base.constants.constants import ArmorTypeIntEnum


def migrate(apps, schema_editor):
    Armor = apps.get_model('base', 'Armor')
    for armor in Armor.objects.all():
        armor.damage_dice_int = (
            ArmorTypeIntEnum[armor.armor_type] if armor.armor_type else None
        )
        armor.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_armor_armor_type_int'),
    ]

    operations = [migrations.RunPython(migrate)]