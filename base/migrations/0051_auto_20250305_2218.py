from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    Subclass = apps.get_model('base', 'Subclass')
    Class = apps.get_model('base', 'Class')
    AvailabilityCondition = apps.get_model('base', 'AvailabilityCondition')
    ShieldType = apps.get_model('base', 'ShieldType')
    for s in Subclass.objects.all():
        for shield in s.shields or []:
            if not int(shield):
                continue
            s.shields_m2m.add(ShieldType.objects.get(base_shield_type=shield))

    for c in Class.objects.all():
        for shield in c.shields or []:
            if not int(shield):
                continue
            c.shields_m2m.add(ShieldType.objects.get(base_shield_type=shield))

    for ac in AvailabilityCondition.objects.all():
        for shield in ac.shields or []:
            if not int(shield):
                continue
            ac.shields_m2m.add(ShieldType.objects.get(base_shield_type=shield))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0050_availabilitycondition_shields_m2m_class_shields_m2m_and_more'),
    ]

    operations = [migrations.RunPython(fill_data)]
