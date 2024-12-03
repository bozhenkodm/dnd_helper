from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import AbilityEnum
from base.helpers import modifier
from base.objects.abilities import Abilities
from base.objects.races import Race


class Ability(models.Model):
    class Meta:
        ordering = ('ordering',)

    title = models.CharField(
        choices=AbilityEnum.generate_choices(),
        max_length=AbilityEnum.max_length(),
        primary_key=True,
    )
    ordering = models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return self.get_title_display()


class NPCAbilityAbstract(models.Model):
    class Meta:
        abstract = True

    half_level: int
    race_data_instance: Race
    _tier: int

    base_strength = models.SmallIntegerField(verbose_name='Сила (базовая)', default=10)
    base_constitution = models.SmallIntegerField(
        verbose_name='Телосложение (базовое)', default=10
    )
    base_dexterity = models.SmallIntegerField(
        verbose_name='Ловкость (базовая)', default=10
    )
    base_intelligence = models.SmallIntegerField(
        verbose_name='Интеллект (базовый)', default=10
    )
    base_wisdom = models.SmallIntegerField(
        verbose_name='Мудрость (базовая)', default=10
    )
    base_charisma = models.SmallIntegerField(
        verbose_name='Харизма (базовая)', default=10
    )
    var_bonus_ability = models.ForeignKey(
        Ability,
        on_delete=models.SET_NULL,
        verbose_name='Выборочный бонус характеристики',
        null=True,
    )
    base_attack_ability = models.CharField(
        verbose_name=_('Base attack ability'),
        choices=AbilityEnum.generate_choices(is_sorted=False),
        max_length=AbilityEnum.max_length(),
        null=True,
        blank=True,
    )

    level4_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 4 уровне',
        choices=AbilityEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level8_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 8 уровне',
        choices=AbilityEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level14_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 14 уровне',
        choices=AbilityEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level18_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 18 уровне',
        choices=AbilityEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level24_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 24 уровне',
        choices=AbilityEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level28_bonus_abilities = MultiSelectField(
        verbose_name='Бонус характеристики на 28 уровне',
        choices=AbilityEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )

    @property
    def _initial_abilities_bonuses(self) -> Abilities:
        # getting one of variable ability bonus for specific npc
        if not self.var_bonus_ability:
            return self.race_data_instance.const_ability_bonus
        var_bonus_abilitiy_name = self.var_bonus_ability.title.lower()
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
        return Abilities(**{ability.lvalue: self._tier for ability in AbilityEnum})

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

    def _calculate_ability_bonus(self, ability: AbilityEnum) -> int:
        abilities = (
            self._initial_abilities_bonuses
            + self._tier_attrs_bonus
            + self._level_abilities_bonuses
            + self._base_abilities
        )
        return getattr(abilities, ability.lvalue)

    @property
    def strength(self) -> int:
        return self._calculate_ability_bonus(AbilityEnum.STRENGTH)

    @property
    def constitution(self) -> int:
        return self._calculate_ability_bonus(AbilityEnum.CONSTITUTION)

    @property
    def dexterity(self) -> int:
        return self._calculate_ability_bonus(AbilityEnum.DEXTERITY)

    @property
    def intelligence(self) -> int:
        return self._calculate_ability_bonus(AbilityEnum.INTELLIGENCE)

    @property
    def wisdom(self) -> int:
        return self._calculate_ability_bonus(AbilityEnum.WISDOM)

    @property
    def charisma(self) -> int:
        return self._calculate_ability_bonus(AbilityEnum.CHARISMA)

    @property
    def str_mod(self) -> int:
        return modifier(self.strength)

    @property
    def con_mod(self) -> int:
        return modifier(self.constitution)

    @property
    def dex_mod(self) -> int:
        return modifier(self.dexterity)

    @property
    def int_mod(self) -> int:
        return modifier(self.intelligence)

    @property
    def wis_mod(self) -> int:
        return modifier(self.wisdom)

    @property
    def cha_mod(self) -> int:
        return modifier(self.charisma)

    def get_ability_text(self, ability: AbilityEnum) -> str:
        ability_value = getattr(self, ability.lvalue)
        mod = modifier(ability_value)
        return (
            f'{ability.description[:3]} '  # type: ignore
            f'{ability_value} ({mod + self.half_level})'
        )

    @property
    def abilities_texts(self) -> list[str]:
        return list(self.get_ability_text(ability) for ability in AbilityEnum)
