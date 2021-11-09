from collections import Counter

from base.constants.constants import AttributeEnum
from base.objects.abilities import Abilities


class AttributeMixin:
    @property
    def _initial_attr_bonuses(self) -> Abilities:
        # getting one of variable ability bonus for specific npc
        var_bonus_attr_name = self.var_bonus_attr.lower()
        return self.race.data_instance.const_ability_bonus + Abilities(
            **{
                var_bonus_attr_name: getattr(
                    self.race.data_instance.var_ability_bonus, var_bonus_attr_name
                )
            }
        )

    @property
    def _level_attr_bonuses(self) -> Abilities:
        result = Abilities()
        for i in (
            4,
            8,
            14,
            18,
            24,
            28,
        ):  # level bonus abilities on 4, 8, 14, 18, 24, 28 levels
            result += Abilities(
                **{
                    ability.lower(): 1
                    for ability in getattr(self, f'level{i}_bonus_attrs')
                }
            )
        return result

    @staticmethod
    def _modifier(value):
        return (value - 10) // 2

    @property
    def _tier_attrs_bonus(self) -> Abilities:
        return Abilities(**{attribute.lname: self._tier for attribute in AttributeEnum})

    @property
    def _base_abilities(self) -> Abilities:
        return Abilities(
            strength=self.base_strength,
            constitution=self.base_constitution,
            dexterity=self.base_dexterity,
            intelligence=self.base_intelligence,
            wisdom=self.base_wisdom,
            charisma=self.base_charisma,
        )

    def _calculate_attribute_bonus(self, attribute: AttributeEnum):
        abilities = (
            self._initial_attr_bonuses
            + self._tier_attrs_bonus
            + self._level_attr_bonuses
            + self._base_abilities
        )
        return getattr(abilities, attribute.lname)

    @property
    def strength(self):
        return self._calculate_attribute_bonus(AttributeEnum.STRENGTH)

    @property
    def constitution(self):
        return self._calculate_attribute_bonus(AttributeEnum.CONSTITUTION)

    @property
    def dexterity(self):
        return self._calculate_attribute_bonus(AttributeEnum.DEXTERITY)

    @property
    def intelligence(self):
        return self._calculate_attribute_bonus(AttributeEnum.INTELLIGENCE)

    @property
    def wisdom(self):
        return self._calculate_attribute_bonus(AttributeEnum.WISDOM)

    @property
    def charisma(self):
        return self._calculate_attribute_bonus(AttributeEnum.CHARISMA)

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

    def get_attribute_text(self, attribute: AttributeEnum) -> str:
        attribute_value = getattr(self, attribute.lname)
        modifier = self._modifier(attribute_value)
        return f'{attribute.value[:3]} {attribute_value} ({modifier + self.half_level})'

    @property
    def attributes_texts(self) -> list:
        return list(self.get_attribute_text(attr) for attr in AttributeEnum)
