from base.constants.constants import NPCClassEnum, ShieldTypeIntEnum
from base.helpers import modifier
from base.objects.npc_classes import NPCClass
from base.objects.races import Race

INITIAL_DEFENCE_VALUE = 10


class NPCDefenceMixin:
    klass_data_instance: NPCClass
    race_data_instance: Race
    half_level: int
    _level_bonus: int
    _tier: int
    strength: int
    constitution: int
    dexterity: int
    intelligence: int
    wisdom: int
    charisma: int

    @property
    def shield(self) -> ShieldTypeIntEnum:
        if not self.arms_slot:  # type: ignore
            return ShieldTypeIntEnum.NONE
        return ShieldTypeIntEnum.get_by_value(self.arms_slot.shield)  # type: ignore

    @property
    def _shield_bonus(self) -> int:
        if self.shield not in self.klass_data_instance.available_shield_types:
            return 0
        return self.shield.value

    @property
    def _defence_level_bonus(self) -> int:
        return INITIAL_DEFENCE_VALUE + self.half_level + self._level_bonus

    @property
    def _necklace_defence_bonus(self) -> int:
        if not self.neck_slot:  # type: ignore
            return 0
        return self.neck_slot.defence_bonus  # type: ignore

    @property
    def armor_class(self) -> int:
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
    def fortitude(self) -> int:
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
    def reflex(self) -> int:
        result = (
            self._defence_level_bonus
            + max(map(modifier, (self.dexterity, self.intelligence)))
            + (self.functional_template.reflex_bonus if self.functional_template else 0)
            + self.race_data_instance.reflex
            + self.klass_data_instance.reflex
            + self._necklace_defence_bonus
        )
        result += self._shield_bonus
        if self.klass.name == NPCClassEnum.BARBARIAN:
            if not self.shield and self.armor.is_light:
                result += self._tier + 1
        return result

    @property
    def will(self) -> int:
        return (
            self._defence_level_bonus
            + max(map(modifier, (self.wisdom, self.charisma)))
            + (self.functional_template.will_bonus if self.functional_template else 0)
            + self.race_data_instance.will
            + self.klass_data_instance.will
            + self._necklace_defence_bonus
        )
