from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    WeaponState = apps.get_model('base', 'WeaponState')
    WeaponHandedness = apps.get_model('base', 'WeaponHandedness')
    for ws in WeaponState.objects.all():
        for h in ws.handedness or []:
            ws.handedness_m2m.add(WeaponHandedness.objects.get(name=h))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0061_weaponstate_handedness_m2m'),
    ]

    operations = [migrations.RunPython(fill_data)]
