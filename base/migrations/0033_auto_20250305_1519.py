from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    MagicArmorType = apps.get_model('base', 'MagicArmorType')
    BaseArmorType = apps.get_model('base', 'BaseArmorType')
    for mat in MagicArmorType.objects.all():
        for at in mat.armor_type_slots:
            mat.armor_type_slots_m2m.add(BaseArmorType.objects.get(armor_class=at))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_magicarmortype_armor_type_slots_m2m'),
    ]

    operations = [migrations.RunPython(fill_data)]
