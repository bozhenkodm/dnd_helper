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
    from base.models.models import FunctionalTemplate, Class, Armor

from base.constants.constants import DefenceTypeEnum, NPCClassEnum, ShieldTypeIntEnum
from base.objects.npc_classes import NPCClass

INITIAL_DEFENCE_VALUE = 10


class NPCProtocol(Protocol):
    klass_data_instance: NPCClass
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


class NPCDefenceMixin:
    @property
    def shield(self: NPCProtocol) -> ShieldTypeIntEnum:
        if not self.arms_slot:
            return ShieldTypeIntEnum.NONE
        return ShieldTypeIntEnum(self.arms_slot.shield)

    @property
    def _shield_bonus(self: NPCProtocol) -> int:
        if self.shield not in self.klass.available_shields:
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
    def armor_class(self: NPCProtocol) -> int:
        result = (
            self._defence_level_bonus
            + (
                self.functional_template.armor_class_bonus
                if self.functional_template
                else 0
            )
            + self.klass_data_instance.armor_class_bonus
            + self._shield_bonus
        )
        return result

    @property
    def fortitude(self: NPCProtocol) -> int:
        return (
            self._defence_level_bonus
            + max(self.str_mod, self.con_mod)
            + (
                self.functional_template.fortitude_bonus
                if self.functional_template
                else 0
            )
            + self.calculate_bonus(DefenceTypeEnum.FORTITUDE)
            + self.klass_data_instance.fortitude
            + self._necklace_defence_bonus
            + self.armor.armor_type.fortitude_bonus
            if self.armor is not None
            else 0
        )

    @property
    def reflex(self: NPCProtocol) -> int:
        result = (
            self._defence_level_bonus
            + max(self.dex_mod, self.int_mod)
            + (self.functional_template.reflex_bonus if self.functional_template else 0)
            + self.calculate_bonus(DefenceTypeEnum.REFLEX)
            + self.klass_data_instance.reflex
            + self._necklace_defence_bonus
            + self.armor.armor_type.reflex_bonus
            if self.armor
            else 0
        )
        result += self._shield_bonus
        if self.klass.name == NPCClassEnum.BARBARIAN:
            if not self.shield and self.armor and self.armor.is_light:
                result += self._tier + 1
        return result

    @property
    def will(self: NPCProtocol) -> int:
        return (
            self._defence_level_bonus
            + max(self.wis_mod, self.cha_mod)
            + (self.functional_template.will_bonus if self.functional_template else 0)
            + self.calculate_bonus(DefenceTypeEnum.WILL)
            + self.klass_data_instance.will
            + self._necklace_defence_bonus
            + self.armor.armor_type.will_bonus
            if self.armor
            else 0
        )
