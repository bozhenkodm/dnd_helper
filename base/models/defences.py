from typing import TYPE_CHECKING, Optional

from base.constants.constants import DefenceTypeEnum, NPCClassEnum
from base.models.npc_protocol import NPCProtocol

if TYPE_CHECKING:
    from base.models.items import ShieldType


INITIAL_DEFENCE_VALUE = 10


class NPCDefenceMixin:
    @property
    def shield(self: NPCProtocol) -> Optional['ShieldType']:
        if not self.arms_slot or not self.arms_slot.shield_type:
            return None
        return self.arms_slot.shield_type

    @property
    def _shield_bonus(self: NPCProtocol) -> int:
        if not self.shield or self.shield not in self.available_shield_types:
            return 0
        return self.shield.base_shield_type

    @property
    def _defence_level_bonus(self: NPCProtocol) -> int:
        return INITIAL_DEFENCE_VALUE + self.half_level + self._level_bonus

    @property
    def _necklace_defence_bonus(self: NPCProtocol) -> int:
        if not self.neck_slot:
            return 0
        return self.neck_slot.defence_bonus

    @property
    def _armor_class_ability_bonus(self: NPCProtocol) -> int:
        result = max(self.int_mod, self.dex_mod)
        if (
            self.klass.name == NPCClassEnum.SEEKER
            and self.subclass.slug == 'SPIRITBOND'
            or self.klass.name == NPCClassEnum.SORCERER
            and self.subclass.slug == 'DRAGON_MAGIC'
        ):
            result = max(self.str_mod, result)
        return result

    @property
    def armor_class_bonus(self: NPCProtocol) -> int:
        result = 0
        if self.armor:
            if self.armor.armor_type.base_armor_type in self.available_armor_types:
                result += self.armor.armor_class
            # result += self.npc.enhancement_with_magic_threshold(
            #     self.npc.armor.enhancement
            # )
        if not self.armor or self.armor.is_light:
            result += self._armor_class_ability_bonus
        return result

    @property
    def armor_class(self: NPCProtocol) -> int:
        return (
            self._defence_level_bonus
            + (
                self.functional_template.armor_class_bonus
                if self.functional_template
                else 0
            )
            + self.armor_class_bonus
            + self._shield_bonus
            + self.calculate_bonus(DefenceTypeEnum.ARMOR_CLASS)
        )

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
            + self.klass.fortitude
            + self._necklace_defence_bonus
            + (self.armor.armor_type.fortitude_bonus if self.armor is not None else 0)
        )

    @property
    def reflex(self: NPCProtocol) -> int:
        return (
            self._defence_level_bonus
            + max(self.dex_mod, self.int_mod)
            + (self.functional_template.reflex_bonus if self.functional_template else 0)
            + self.calculate_bonus(DefenceTypeEnum.REFLEX)
            + self.klass.reflex
            + self._necklace_defence_bonus
            + (self.armor.armor_type.reflex_bonus if self.armor else 0)
            + self._shield_bonus
        )

    @property
    def will(self: NPCProtocol) -> int:
        return (
            self._defence_level_bonus
            + max(self.wis_mod, self.cha_mod)
            + (self.functional_template.will_bonus if self.functional_template else 0)
            + self.calculate_bonus(DefenceTypeEnum.WILL)
            + self.klass.will
            + self._necklace_defence_bonus
            + (self.armor.armor_type.will_bonus if self.armor else 0)
        )
