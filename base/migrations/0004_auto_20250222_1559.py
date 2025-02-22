# Generated by Django 5.1.6 on 2025-02-22 15:59

from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    WeaponState = apps.get_model('base', 'WeaponState')
    WeaponGroup = apps.get_model('base', 'WeaponGroup')
    for ws in WeaponState.objects.all():
        for g in ws.group:
            ws.groups.add(WeaponGroup.objects.get(name=g))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_weaponstate_groups'),
    ]

    operations = [migrations.RunPython(fill_data)]
