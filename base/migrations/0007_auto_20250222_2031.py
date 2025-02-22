# Generated by Django 5.1.6 on 2025-02-22 20:31

from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    MagicWeaponType = apps.get_model('base', 'MagicWeaponType')
    WeaponGroup = apps.get_model('base', 'WeaponGroup')
    for mwt in MagicWeaponType.objects.all():
        for wg in mwt.weapon_groups:
            mwt.weapon_groups_m2m.add(WeaponGroup.objects.get(name=wg))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_weapontype_group_and_more'),
    ]

    operations = [migrations.RunPython(fill_data)]
