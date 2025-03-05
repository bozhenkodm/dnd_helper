from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    MagicWeaponType = apps.get_model('base', 'MagicWeaponType')
    WeaponCategory = apps.get_model('base', 'WeaponCategory')
    for mwt in MagicWeaponType.objects.all():
        for ct in mwt.weapon_categories or []:
            mwt.weapon_categories_m2m.add(WeaponCategory.objects.get(code=int(ct)))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_magicweapontype_weapon_categories_m2m'),
    ]

    operations = [migrations.RunPython(fill_data)]
