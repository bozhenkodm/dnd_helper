from django.db import migrations

from base.constants.constants import WeaponCategoryIntEnum


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    WeaponCategory = apps.get_model('base', 'WeaponCategory')
    for wci in WeaponCategoryIntEnum:
        wc = WeaponCategory(
            code=wci,
            is_ranged=(3 < wci < 7),
            category=((wci % 3) if wci != 7 else None),
        )
        wc.save()
    WeaponType = apps.get_model('base', 'WeaponType')
    for wt in WeaponType.objects.all():
        wt.category_fk = WeaponCategory.objects.get(code=wt.category)
        wt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_weaponcategory_category'),
    ]

    operations = [migrations.RunPython(fill_data)]
