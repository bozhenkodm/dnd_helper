from base.constants.constants import AbilitiesEnum
from base.helpers import modifier
from base.objects.abilities import Abilities


class AttributeMixin:
    @property
    def _initial_attr_bonuses(self) -> Abilities:
        # getting one of variable ability bonus for specific npc
        if not self.var_bonus_attr:
            return self.race_data_instance.const_ability_bonus
        var_bonus_attr_name = self.var_bonus_attr.lower()
        return self.race_data_instance.const_ability_bonus + Abilities(
            **{
                var_bonus_attr_name: getattr(
                    self.race_data_instance.var_ability_bonus, var_bonus_attr_name
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

    @property
    def _tier_attrs_bonus(self) -> Abilities:
        return Abilities(**{ability.lvalue: self._tier for ability in AbilitiesEnum})

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

    def _calculate_ability_bonus(self, ability: AbilitiesEnum):
        abilities = (
            self._initial_attr_bonuses
            + self._tier_attrs_bonus
            + self._level_attr_bonuses
            + self._base_abilities
        )
        return getattr(abilities, ability.lvalue)

    @property
    def strength(self):
        return self._calculate_ability_bonus(AbilitiesEnum.STRENGTH)

    @property
    def constitution(self):
        return self._calculate_ability_bonus(AbilitiesEnum.CONSTITUTION)

    @property
    def dexterity(self):
        return self._calculate_ability_bonus(AbilitiesEnum.DEXTERITY)

    @property
    def intelligence(self):
        return self._calculate_ability_bonus(AbilitiesEnum.INTELLIGENCE)

    @property
    def wisdom(self):
        return self._calculate_ability_bonus(AbilitiesEnum.WISDOM)

    @property
    def charisma(self):
        return self._calculate_ability_bonus(AbilitiesEnum.CHARISMA)

    @property
    def str_mod(self):
        return modifier(self.strength)

    @property
    def con_mod(self):
        return modifier(self.constitution)

    @property
    def dex_mod(self):
        return modifier(self.dexterity)

    @property
    def int_mod(self):
        return modifier(self.intelligence)

    @property
    def wis_mod(self):
        return modifier(self.wisdom)

    @property
    def cha_mod(self):
        return modifier(self.charisma)

    def get_ability_text(self, ability: AbilitiesEnum) -> str:
        ability_value = getattr(self, ability.lvalue)
        mod = modifier(ability_value)
        return f'{ability.value[:3]} {ability_value} ({mod + self.half_level})'

    @property
    def abilities_texts(self) -> list:
        return list(self.get_ability_text(ability) for ability in AbilitiesEnum)
