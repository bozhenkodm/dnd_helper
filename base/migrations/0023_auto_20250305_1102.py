from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    Ability = apps.get_model('base', 'Ability')
    Power = apps.get_model('base', 'Power')
    for p in Power.objects.all():
        if p.attack_ability:
            p.attack_ability_fk = Ability.objects.get(title=p.attack_ability)
            p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_power_attack_ability_fk'),
    ]

    operations = [migrations.RunPython(fill_data)]
