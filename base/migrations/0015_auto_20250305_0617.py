from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    Subclass = apps.get_model('base', 'Subclass')
    Class = apps.get_model('base', 'Class')
    WeaponCategory = apps.get_model('base', 'WeaponCategory')
    for c in Class.objects.all():
        for ct in c.weapon_categories or []:
            c.weapon_categories_m2m.add(WeaponCategory.objects.get(code=int(ct)))
    for c in Subclass.objects.all():
        for ct in c.weapon_categories or []:
            c.weapon_categories_m2m.add(WeaponCategory.objects.get(code=int(ct)))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_availabilitycondition_weapon_categories_m2m_and_more'),
    ]

    operations = [migrations.RunPython(fill_data)]
