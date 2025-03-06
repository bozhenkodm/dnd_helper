from django.db import migrations

from base.constants.constants import WeaponHandednessEnum


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    WeaponType = apps.get_model('base', 'WeaponType')
    WeaponHandedness = apps.get_model('base', 'WeaponHandedness')
    whs = []
    for whe in WeaponHandednessEnum:
        one_hand = True
        if whe == WeaponHandednessEnum.TWO:
            one_hand = False
        if whe == WeaponHandednessEnum.FREE:
            one_hand = None
        whs.append(WeaponHandedness(name=whe.value, is_one_handed=one_hand))
    WeaponHandedness.objects.bulk_create(whs)
    for wt in WeaponType.objects.all():
        wt.handedness_fk = WeaponHandedness.objects.get(name=wt.handedness)
        wt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0055_weapontype_handedness_fk_and_more'),
    ]

    operations = [migrations.RunPython(fill_data)]
