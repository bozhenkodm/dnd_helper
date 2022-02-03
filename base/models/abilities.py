from django.db import models
from multiselectfield import MultiSelectField  # type: ignore

from base.constants.constants import AbilitiesEnum
from base.helpers import modifier
from base.objects.abilities import Abilities
from base.objects.races import Race


class AttributeAbstract(models.Model):
    class Meta:
        abstract = True

    half_level: int
    race_data_instance: Race
    _tier: int

    base_strength = models.SmallIntegerField(verbose_name='Сила (базовая)')
    base_constitution = models.SmallIntegerField(
        verbose_name='Телосложение (базовое)',
    )
    base_dexterity = models.SmallIntegerField(
        verbose_name='Ловкость (базовая)',
    )
    base_intelligence = models.SmallIntegerField(
        verbose_name='Интеллект (базовый)',
    )
    base_wisdom = models.SmallIntegerField(
        verbose_name='Мудрость (базовая)',
    )
    base_charisma = models.SmallIntegerField(
        verbose_name='Харизма (базовая)',
    )
    var_bonus_ability = models.CharField(
        verbose_name='Выборочный бонус характеристики',
        max_length=AbilitiesEnum.max_length(),
        null=True,
        blank=True,
    )
    base_attack_ability = MultiSelectField(
        verbose_name='Атакующие характеристики',
        choices=AbilitiesEnum.generate_choices(is_sorted=False),
        null=True,
        blank=True,
    )

    level4_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 4 уровне',
        choices=AbilitiesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level8_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 8 уровне',
        choices=AbilitiesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level14_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 14 уровне',
        choices=AbilitiesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level18_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 18 уровне',
        choices=AbilitiesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level24_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 24 уровне',
        choices=AbilitiesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level28_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 28 уровне',
        choices=AbilitiesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )

    @property
    def _initial_abilities_bonuses(self) -> Abilities:
        # getting one of variable ability bonus for specific npc
        if not self.var_bonus_ability:
            return self.race_data_instance.const_ability_bonus
        var_bonus_abilitiy_name = self.var_bonus_ability.lower()
        return self.race_data_instance.const_ability_bonus + Abilities(
            **{
                var_bonus_abilitiy_name: getattr(
                    self.race_data_instance.var_ability_bonus, var_bonus_abilitiy_name
                )
            }
        )

    @property
    def _level_abilities_bonuses(self) -> Abilities:
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
                    for ability in getattr(self, f'level{i}_bonus_abilities')
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
            self._initial_abilities_bonuses
            + self._tier_attrs_bonus
            + self._level_abilities_bonuses
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
        return (
            f'{ability.description[:3]} '  # type: ignore
            f'{ability_value} ({mod + self.half_level})'
        )

    @property
    def abilities_texts(self) -> list:
        return list(self.get_ability_text(ability) for ability in AbilitiesEnum)
