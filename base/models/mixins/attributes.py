from collections import Counter

from base.constants import AttributesEnum


class AttributeMixin:
    @property
    def _initial_attr_bonuses(self):
        bonus_attrs = self.race.const_bonus_attrs
        bonus_attrs.append(self.var_bonus_attr)
        bonus_attrs = {key: 2 for key in bonus_attrs}
        return bonus_attrs

    @property
    def _level_attr_bonuses(self):
        bonus_attrs = (
            (self.level4_bonus_attrs or [])
            + (self.level8_bonus_attrs or [])
            + (self.level14_bonus_attrs or [])
            + (self.level18_bonus_attrs or [])
            + (self.level24_bonus_attrs or [])
            + (self.level28_bonus_attrs or [])
        )
        return Counter(bonus_attrs)

    @staticmethod
    def _modifier(value):
        return (value - 10) // 2

    @property
    def _tier_attrs_bonus(self):
        return self._tier

    def _calculate_attribute_bonus(self, attribute: AttributesEnum):
        return (
            self._initial_attr_bonuses.get(attribute.name, 0)
            + self._tier_attrs_bonus
            + self._level_attr_bonuses[attribute.name]
        )

    @property
    def strength(self):
        return self.base_strength + self._calculate_attribute_bonus(
            AttributesEnum.STRENGTH
        )

    @property
    def constitution(self):
        return self.base_constitution + self._calculate_attribute_bonus(
            AttributesEnum.CONSTITUTION
        )

    @property
    def dexterity(self):
        return self.base_dexterity + self._calculate_attribute_bonus(
            AttributesEnum.DEXTERITY
        )

    @property
    def intelligence(self):
        return self.base_intelligence + self._calculate_attribute_bonus(
            AttributesEnum.INTELLIGENCE
        )

    @property
    def wisdom(self):
        return self.base_wisdom + self._calculate_attribute_bonus(AttributesEnum.WISDOM)

    @property
    def charisma(self):
        return self.base_charisma + self._calculate_attribute_bonus(
            AttributesEnum.CHARISMA
        )

    @property
    def str_mod(self):
        return self._modifier(self.strength)

    @property
    def con_mod(self):
        return self._modifier(self.constitution)

    @property
    def dex_mod(self):
        return self._modifier(self.dexterity)

    @property
    def int_mod(self):
        return self._modifier(self.intelligence)

    @property
    def wis_mod(self):
        return self._modifier(self.wisdom)

    @property
    def cha_mod(self):
        return self._modifier(self.charisma)

    def get_attribute_text(self, attribute: AttributesEnum):
        attribute_value = getattr(self, attribute.lname)
        modifier = self._modifier(attribute_value)
        return f'{attribute.value[:3]} {attribute_value} ({modifier + self.half_level})'

    @property
    def attributes_texts(self) -> list:
        return list(self.get_attribute_text(attr) for attr in AttributesEnum)
