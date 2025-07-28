from typing import TYPE_CHECKING, Optional

from base.constants.constants import DefenceTypeEnum, NPCClassEnum
from base.models.npc_protocol import NPCProtocol

if TYPE_CHECKING:
    from base.models.items import ShieldType


# Base defence value used in D&D 4th edition - all defences start at 10
INITIAL_DEFENCE_VALUE = 10


class NPCDefenceMixin:
    """
    Mixin class that provides defence calculation methods for NPCs.

    This class implements the D&D 4th edition defence system with four main defences:
    - Armor Class (AC): Protection against physical attacks
    - Fortitude: Resistance to physical effects (poison, disease, etc.)
    - Reflex: Ability to dodge area effects and some ranged attacks
    - Will: Mental resistance to charm, fear, and psychic effects

    Each defence is calculated using a base value (10 + half level + level bonus)
    plus relevant ability modifiers and equipment bonuses.
    """

    @property
    def shield(self: NPCProtocol) -> Optional['ShieldType']:
        """Get the shield equipped in the arms slot, if any."""
        if not self.arms_slot or not self.arms_slot.shield_type:
            return None
        return self.arms_slot.shield_type

    @property
    def _shield_bonus(self: NPCProtocol) -> int:
        """Calculate the defence bonus provided by an equipped shield.

        Returns:
            Shield's base defence bonus if equipped and available to this NPC,
            otherwise 0.
        """
        if not self.shield or self.shield not in self.available_shield_types:
            return 0
        return self.shield.base_shield_type

    @property
    def _defence_level_bonus(self: NPCProtocol) -> int:
        """Calculate the base defence bonus from level.

        This is the foundation for all defences in D&D 4e:
        10 (base) + half level + level-dependent bonus
        """
        return INITIAL_DEFENCE_VALUE + self.half_level + self._level_bonus

    @property
    def _necklace_defence_bonus(self: NPCProtocol) -> int:
        """Get the defence bonus from equipped neck slot item (amulet, etc.)."""
        if not self.neck_slot:
            return 0
        return self.neck_slot.defence_bonus

    @property
    def _armor_class_ability_bonus(self: NPCProtocol) -> int:
        """Calculate ability modifier bonus for Armor Class.

        Standard rule: Use the higher of Intelligence or Dexterity modifier.
        Special cases:
        - Seeker (Spiritbond): Can also use Strength modifier
        - Sorcerer (Dragon Magic): Can also use Strength modifier
        """
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
        """Calculate the total armor bonus to AC.

        Includes:
        - Base armor AC bonus (if armor is available to this NPC)
        - Ability modifier bonus (for no armor or light armor only)

        Note: Enhancement bonuses are commented out but could be added later.
        """
        result = 0
        if self.armor:
            if self.armor.armor_type.base_armor_type in self.available_armor_types:
                result += self.armor.armor_class
            # result += self.npc.enhancement_with_magic_threshold(
            #     self.npc.armor.enhancement
            # )
        # Only add ability bonus if wearing no armor or light armor
        if not self.armor or self.armor.is_light:
            result += self._armor_class_ability_bonus
        return result

    @property
    def armor_class(self: NPCProtocol) -> int:
        """Calculate total Armor Class defence.

        AC protects against physical attacks and is calculated as:
        - Base defence (10 + half level + level bonus)
        - Functional template AC bonus (if any)
        - Armor and ability modifier bonuses
        - Shield bonus
        - Miscellaneous AC bonuses from powers, items, etc.
        """
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
        """Calculate total Fortitude defence.

        Fortitude resists physical effects like poison, disease, and death.
        Calculated as:
        - Base defence (10 + half level + level bonus)
        - Higher of Strength or Constitution modifier
        - Functional template bonus (if any)
        - Miscellaneous bonuses from powers, items, etc.
        - Class-specific fortitude bonus
        - Neck slot item bonus
        - Armor type fortitude bonus
        """
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
        """Calculate total Reflex defence.

        Reflex helps avoid area effects and ranged attacks.
        Calculated as:
        - Base defence (10 + half level + level bonus)
        - Higher of Dexterity or Intelligence modifier
        - Functional template bonus (if any)
        - Miscellaneous bonuses from powers, items, etc.
        - Class-specific reflex bonus
        - Neck slot item bonus
        - Armor type reflex bonus
        - Shield bonus (shields help deflect area effects)
        """
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
        """Calculate total Will defence.

        Will resists mental effects like charm, fear, and psychic attacks.
        Calculated as:
        - Base defence (10 + half level + level bonus)
        - Higher of Wisdom or Charisma modifier
        - Functional template bonus (if any)
        - Miscellaneous bonuses from powers, items, etc.
        - Class-specific will bonus
        - Neck slot item bonus
        - Armor type will bonus (some armor provides mental protection)
        """
        return (
            self._defence_level_bonus
            + max(self.wis_mod, self.cha_mod)
            + (self.functional_template.will_bonus if self.functional_template else 0)
            + self.calculate_bonus(DefenceTypeEnum.WILL)
            + self.klass.will
            + self._necklace_defence_bonus
            + (self.armor.armor_type.will_bonus if self.armor else 0)
        )
