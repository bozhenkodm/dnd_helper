from base.constants.constants import NPCClassIntEnum, ShieldTypeEnum
from base.helpers import modifier

INITIAL_DEFENCE_VALUE = 10


class DefenceMixin:
    @property
    def _shield_bonus(self):
        if (
            not self.shield
            or self.shield not in self.klass_data_instance.available_shield_types
        ):
            return 0
        if self.shield == ShieldTypeEnum.LIGHT:
            return 1
        return 2

    @property
    def _defence_level_bonus(self):
        return INITIAL_DEFENCE_VALUE + self.half_level + self._level_bonus

    @property
    def _necklace_defence_bonus(self) -> int:
        if not self.neck_slot:
            return 0
        return self.neck_slot.defence_bonus

    @property
    def armor_class(self):
        result = (
            self._defence_level_bonus
            + self.race_data_instance.armor_class
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
    def fortitude(self):
        return (
            self._defence_level_bonus
            + max(map(modifier, (self.strength, self.constitution)))
            + (
                self.functional_template.fortitude_bonus
                if self.functional_template
                else 0
            )
            + self.race_data_instance.fortitude
            + self.klass_data_instance.fortitude
            + self._necklace_defence_bonus
        )

    @property
    def reflex(self):
        result = (
            self._defence_level_bonus
            + max(map(modifier, (self.dexterity, self.intelligence)))
            + (self.functional_template.reflex_bonus if self.functional_template else 0)
            + self.race_data_instance.reflex
            + self.klass_data_instance.reflex
            + self._necklace_defence_bonus
        )
        result += self._shield_bonus
        if self.klass.name == NPCClassIntEnum.BARBARIAN:
            if not self.shield and self.armor.is_light:
                result += self._tier + 1
        return result

    @property
    def will(self):
        return (
            self._defence_level_bonus
            + max(map(modifier, (self.wisdom, self.charisma)))
            + (self.functional_template.will_bonus if self.functional_template else 0)
            + self.race_data_instance.will
            + self.klass_data_instance.will
            + self._necklace_defence_bonus
        )
