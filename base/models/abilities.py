from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import AbilityEnum
from base.helpers import modifier
from base.objects.abilities import Abilities


class Ability(models.Model):
    title = models.CharField(
        choices=AbilityEnum.generate_choices(),
        max_length=AbilityEnum.max_length(),
        unique=True,
    )

    def __str__(self) -> str:
        return self.get_title_display()


class NPCAbilityAbstract(models.Model):
    class Meta:
        abstract = True

    half_level: int
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
        verbose_name=_('Selective ability bonus'),
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
        const_ability_bonus = Abilities.init_with_const(
            *[
                AbilityEnum(a)
                for a in self.race.const_ability_bonus.values_list('title', flat=True)
            ],
            value=2,
        )
        if self.var_bonus_ability:
            var_ability_bonus = Abilities.init_with_const(
                AbilityEnum(self.var_bonus_ability.title), value=2
            )
        else:
            var_ability_bonus = Abilities()
        return const_ability_bonus + var_ability_bonus

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
            result += Abilities.init_with_const(
                *(
                    AbilityEnum(ability)
                    for ability in getattr(self, f'level{i}_bonus_abilities')
                ),
                value=1,
            )
        return result

    @property
    def _tier_attrs_bonus(self) -> Abilities:
        return Abilities.init_with_const(*AbilityEnum, value=self._tier)

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

    @property
    def _abilities(self) -> Abilities:
        return (
            self._initial_abilities_bonuses
            + self._tier_attrs_bonus
            + self._level_abilities_bonuses
            + self._base_abilities
        )

    @property
    def strength(self) -> int:
        return self._abilities.strength

    @property
    def constitution(self) -> int:
        return self._abilities.constitution

    @property
    def dexterity(self) -> int:
        return self._abilities.dexterity

    @property
    def intelligence(self) -> int:
        return self._abilities.intelligence

    @property
    def wisdom(self) -> int:
        return self._abilities.wisdom

    @property
    def charisma(self) -> int:
        return self._abilities.charisma

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
