# Generated by Django 5.1.6 on 2025-03-05 21:58

from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    ItemState = apps.get_model('base', 'ItemState')
    ShieldType = apps.get_model('base', 'ShieldType')
    for its in ItemState.objects.all():
        for shield in its.shield or []:
            if int(shield):
                its.shield_m2m.add(ShieldType.objects.get(base_shield_type=int(shield)))


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0046_itemstate_shield_m2m'),
    ]

    operations = [migrations.RunPython(fill_data)]
