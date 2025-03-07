from django.db import migrations

from base.constants.constants import ArmorTypeIntEnum


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    BaseArmorType = apps.get_model('base', 'BaseArmorType')
    # bats = []
    # for at in (0, 2, 3, 6, 7, 8):
    #     print('1' * 88)
    #     skill_penalty = 0
    #     if at == ArmorTypeIntEnum.PLATE:
    #         skill_penalty = 2
    #     if at in (ArmorTypeIntEnum.CHAINMAIL, ArmorTypeIntEnum.HIDE):
    #         skill_penalty = 1
    #     print('1' * 88)
    #     bat = BaseArmorType(
    #         armor_class=at,
    #         is_light=(at <= 3),
    #         speed_penalty=(at > 3),
    #         skill_penalty=skill_penalty,
    #     )
    #     bats.append(bat)
    #     print('1' * 88)
    #     # bat.save()
    #     print('1' * 88)
    # BaseArmorType.objects.bulk_create(bats)

    ArmorType = apps.get_model('base', 'ArmorType')
    for at in ArmorType.objects.all():
        at.base_armor_type_fk = BaseArmorType.objects.get(
            armor_class=at.base_armor_type
        )
        at.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_alter_basearmortype_armor_class'),
    ]

    operations = [migrations.RunPython(fill_data)]
