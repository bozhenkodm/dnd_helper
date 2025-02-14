from django.contrib import admin

from base.admin.admin_classes import (
    ArmorAdmin,
    ArmorTypeAdmin,
    ArmsItemSlotAdmin,
    MagicArmItemTypeAdmin,
    MagicArmorTypeAdmin,
    MagicItemAdmin,
    MagicItemTypeAdmin,
    MagicWeaponTypeAdmin,
    WeaponAdmin,
    WeaponTypeAdmin,
)
from items.models import (
    Armor,
    ArmorType,
    ArmsSlotItem,
    MagicArmItemType,
    MagicArmorType,
    MagicItemType,
    MagicWeaponType,
    SimpleMagicItem,
    Weapon,
    WeaponType,
)

admin.site.register(ArmorType, ArmorTypeAdmin)
admin.site.register(WeaponType, WeaponTypeAdmin)
admin.site.register(MagicItemType, MagicItemTypeAdmin)
admin.site.register(MagicArmorType, MagicArmorTypeAdmin)
admin.site.register(MagicWeaponType, MagicWeaponTypeAdmin)
admin.site.register(MagicArmItemType, MagicArmItemTypeAdmin)


# hidden from sidebar
admin.site.register(Armor, ArmorAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(SimpleMagicItem, MagicItemAdmin)
admin.site.register(ArmsSlotItem, ArmsItemSlotAdmin)
