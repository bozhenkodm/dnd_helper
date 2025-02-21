# Generated by Django 5.1.6 on 2025-02-21 15:46

from django.db import migrations

from base.constants.constants import WeaponGroupEnum


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    WeaponType = apps.get_model('base', 'WeaponType')
    WeaponGroup = apps.get_model('base', 'WeaponGroup')
    wgs = []
    for wge in WeaponGroupEnum:
        wgs.append(
            WeaponGroup(
                name=wge.name,
                is_ranged=wge
                in (
                    WeaponGroupEnum.SLING,
                    WeaponGroupEnum.CROSSBOW,
                    WeaponGroupEnum.BOW,
                ),
            )
        )
    WeaponGroup.objects.bulk_create(wgs)
    for wt in WeaponType.objects.all():
        for g in wt.group:
            wg = WeaponGroup.objects.get(name=g)
            wt.groups.add(wg)


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_weapongroup_weapontype_groups'),
    ]

    operations = [migrations.RunPython(fill_data)]
