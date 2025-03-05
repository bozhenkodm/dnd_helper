from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    WeaponState = apps.get_model('base', 'WeaponState')
    WeaponCategory = apps.get_model('base', 'WeaponCategory')
    for ws in WeaponState.objects.all():
        for c in ws.category or []:
            ws.category_m2m.add(WeaponCategory.objects.get(code=int(c)))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_weaponstate_category_m2m'),
    ]

    operations = [migrations.RunPython(fill_data)]
