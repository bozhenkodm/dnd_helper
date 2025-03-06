from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    ShieldType = apps.get_model('base', 'ShieldType')
    MagicArmItemType = apps.get_model('base', 'MagicArmItemType')
    for mait in MagicArmItemType.objects.all():
        for s in mait.shield_slots or []:
            mait.shield_slots_m2m.add(ShieldType.objects.get(base_shield_type=int(s)))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_magicarmitemtype_shield_slots_m2m'),
    ]

    operations = []
