from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    Subclass = apps.get_model('base', 'Subclass')
    Class = apps.get_model('base', 'Class')
    AvailabilityCondition = apps.get_model('base', 'AvailabilityCondition')
    BaseArmorType = apps.get_model('base', 'BaseArmorType')
    for s in Subclass.objects.all():
        for at in s.armor_types or []:
            s.armor_types_m2m.add(BaseArmorType.objects.get(armor_class=at))

    for c in Class.objects.all():
        for at in c.armor_types or []:
            c.armor_types_m2m.add(BaseArmorType.objects.get(armor_class=at))

    for ac in AvailabilityCondition.objects.all():
        for at in ac.armor_types or []:
            ac.armor_types_m2m.add(BaseArmorType.objects.get(armor_class=at))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_availabilitycondition_armor_types_m2m_and_more'),
    ]

    operations = [migrations.RunPython(fill_data)]
