from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from base.models.magic_items import (
        ArmsSlotItem,
        FeetSlotItem,
        HeadSlotItem,
        NeckSlotItem,
        RingsSlotItem,
        WaistSlotItem,
        HandsSlotItem,
    )
    from base.models.models import FunctionalTemplate, Armor
    from base.models.klass import Class

from base.constants.constants import (
    ArmorTypeIntEnum,
    DefenceTypeEnum,
    NPCClassEnum,
    ShieldTypeIntEnum,
    WeaponHandednessEnum,
)

INITIAL_DEFENCE_VALUE = 10


class NPCProtocol(Protocol):
    half_level: int
    _level_bonus: int
    _tier: int
    str_mod: int
    con_mod: int
    dex_mod: int
    int_mod: int
    wis_mod: int
    cha_mod: int
    arms_slot: "ArmsSlotItem"
    neck_slot: "NeckSlotItem"
    head_slot: "HeadSlotItem"
    feet_slot: "FeetSlotItem"
    waist_slot: "WaistSlotItem"
    left_ring_slot: "RingsSlotItem"
    right_ring_slot: "RingsSlotItem"
    gloves_slot: "HandsSlotItem"
    functional_template: "FunctionalTemplate"
    klass: "Class"
    armor: "Armor"

    @property
    def _defence_level_bonus(self) -> int:
        pass

    @property
    def _shield_bonus(self) -> int:
        pass

    @property
    def shield(self) -> ShieldTypeIntEnum:
        pass

    @property
    def _necklace_defence_bonus(self) -> int:
        pass

    def _is_brawler_fighter_and_properly_armed(self) -> bool:
        pass


class NPCDefenceMixin:
    @property
    def shield(self: NPCProtocol) -> ShieldTypeIntEnum:
        if not self.arms_slot:
            return ShieldTypeIntEnum.NONE
        return ShieldTypeIntEnum(self.arms_slot.shield)

    @property
    def _shield_bonus(self: NPCProtocol) -> int:
        if self.shield not in self.klass.shields:
            return 0
        return self.shield.value

    @property
    def _defence_level_bonus(self: NPCProtocol) -> int:
        return INITIAL_DEFENCE_VALUE + self.half_level + self._level_bonus

    @property
    def _necklace_defence_bonus(self: NPCProtocol) -> int:
        if not self.neck_slot:
            return 0
        return self.neck_slot.defence_bonus

    @property
    def _armor_class_ability_bonus(self) -> int:
        result = max(self.int_mod, self.dex_mod)
        if (
            self.klass.name == NPCClassEnum.SEEKER
            and self.subclass.slug == 'SPIRITBOND'
            or self.klass.name == NPCClassEnum.SORCERER
            and self.subclass.slug == 'DRAGON_MAGIC'
        ):
            result = max(self.str_mod, result)
        return result

    def _is_vampire_and_armored_properly(self) -> bool:
        return (
            self.klass.name == NPCClassEnum.VAMPIRE
            and not self.shield
            and (
                not self.armor
                or self.armor.armor_type.base_armor_type == ArmorTypeIntEnum.CLOTH
            )
        )

    def _is_barbarian_and_armored_properly(self) -> bool:
        return (
            self.klass.name == NPCClassEnum.BARBARIAN
            and not self.shield
            and (not self.armor or self.armor.is_light)
        )

    def _is_brawler_fighter_and_properly_armed(self) -> bool:
        # brawler fighter should have melee weapon in just one hand
        if any(
            (
                self.klass.name != NPCClassEnum.FIGHTER,
                self.subclass.slug != 'BRAWLER',
                self.shield,
                self.secondary_hand,
                self.primary_hand and not self.primary_hand.weapon_type.is_melee,
                self.primary_hand
                and self.primary_hand.handedness == WeaponHandednessEnum.TWO,
                self.primary_hand and self.primary_hand.is_double,
            )
        ):
            return False
        return True

    def _is_avenger_and_armored_properly(self) -> bool:
        return (
            self.klass.name == NPCClassEnum.AVENGER
            and not self.shield
            and (
                not self.armor
                or self.armor.armor_type.base_armor_type == ArmorTypeIntEnum.CLOTH
            )
        )

    @property
    def armor_class_bonus(self) -> int:
        result = 0
        if self.armor:
            available_armor_types = self.klass.armor_types + self.subclass.armor_types
            if self.armor.armor_type.base_armor_type in available_armor_types:
                result += self.armor.armor_class
            # result += self.npc.enhancement_with_magic_threshold(
            #     self.npc.armor.enhancement
            # )
        if not self.armor or self.armor.is_light:
            result += self._armor_class_ability_bonus

        if self._is_vampire_and_armored_properly():
            # Рефлексы вампира
            result += 2
        if self._is_barbarian_and_armored_properly():
            result += self._tier + 1
        if self._is_brawler_fighter_and_properly_armed():
            result += 1
        if self._is_avenger_and_armored_properly():
            result += 3
        if self.klass.name == NPCClassEnum.SWORDMAGE:
            if (
                not self.shield
                and not self.secondary_hand
                and self.primary_hand
                and not self.primary_hand.is_double
            ):
                result += 3
            else:
                result += 1
        return result

    @property
    def armor_class(self: NPCProtocol) -> int:
        result = (
            self._defence_level_bonus
            + (
                self.functional_template.armor_class_bonus
                if self.functional_template
                else 0
            )
            + self.armor_class_bonus
            + self._shield_bonus
        )
        return result

    @property
    def fortitude(self: NPCProtocol) -> int:
        result = (
            self._defence_level_bonus
            + max(self.str_mod, self.con_mod)
            + (
                self.functional_template.fortitude_bonus
                if self.functional_template
                else 0
            )
            + self.calculate_bonus(DefenceTypeEnum.FORTITUDE)
            + self.klass.fortitude
            + self._necklace_defence_bonus
            + self.armor.armor_type.fortitude_bonus
            if self.armor is not None
            else 0
        )
        if self._is_brawler_fighter_and_properly_armed():
            result += 2
        return result

    @property
    def reflex(self: NPCProtocol) -> int:
        result = (
            self._defence_level_bonus
            + max(self.dex_mod, self.int_mod)
            + (self.functional_template.reflex_bonus if self.functional_template else 0)
            + self.calculate_bonus(DefenceTypeEnum.REFLEX)
            + self.klass.reflex
            + self._necklace_defence_bonus
            + self.armor.armor_type.reflex_bonus
            if self.armor
            else 0
        )
        result += self._shield_bonus
        if self._is_barbarian_and_armored_properly():
            result += self._tier + 1
        return result

    @property
    def will(self: NPCProtocol) -> int:
        return (
            self._defence_level_bonus
            + max(self.wis_mod, self.cha_mod)
            + (self.functional_template.will_bonus if self.functional_template else 0)
            + self.calculate_bonus(DefenceTypeEnum.WILL)
            + self.klass.will
            + self._necklace_defence_bonus
            + self.armor.armor_type.will_bonus
            if self.armor
            else 0
        )
