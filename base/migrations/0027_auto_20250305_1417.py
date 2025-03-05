from django.db import migrations

from base.constants.constants import ArmorTypeIntEnum


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    BaseArmorType = apps.get_model('base', 'BaseArmorType')
    for at in (0, 2, 3, 6, 7, 8):
        print('1' * 88)
        skill_penalty = 0
        if at == ArmorTypeIntEnum.PLATE:
            skill_penalty = 2
        if at in (ArmorTypeIntEnum.CHAINMAIL, ArmorTypeIntEnum.HIDE):
            skill_penalty = 1
        bat = BaseArmorType(
            armor_class=at.value,
            is_light=(at <= 3),
            speed_penalty=(at > 3),
            skill_penalty=skill_penalty,
        )
        bat.save()
    ArmorType = apps.get_model('base', 'ArmorType')
    for at in ArmorType.objects.all():
        at.base_armor_type_fk = BaseArmorType.objects.get(
            armor_class=at.base_armor_type
        )
        at.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_basearmortype_armortype_base_armor_type_fk'),
    ]

    operations = [migrations.RunPython(fill_data)]
