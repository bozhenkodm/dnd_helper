from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from base.constants.constants import LEVELS_WITH_ABILITY_BONUS, AbilityEnum
from base.helpers import modifier
from base.objects.abilities import Abilities


class AbilityLevelBonus(models.Model):
    class Meta:
        unique_together = ('ability', 'npc', 'level')

    ability = models.ForeignKey(
        'base.Ability', on_delete=models.CASCADE, related_name='level_bonuses'
    )
    npc = models.ForeignKey('base.NPC', on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(
        choices=((i, i) for i in LEVELS_WITH_ABILITY_BONUS)
    )


class Ability(models.Model):
    title = models.CharField(
        choices=AbilityEnum.generate_choices(),
        max_length=AbilityEnum.max_length(),
        unique=True,
    )

    def __str__(self) -> str:
        return self.get_title_display()

    @property
    def name(self) -> str:
        return self.title.lower()

    @property
    def short_name(self) -> str:
        return self.name[:3]

    @property
    def mod(self) -> str:
        return f'{self.short_name}_mod'


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
    level_ability_bonuses = models.ManyToManyField(
        Ability,
        blank=True,
        through=AbilityLevelBonus,
        related_name='npcs_for_level_bonuses',
        verbose_name=_('Ability level bonuses'),
    )

    @property
    def _initial_abilities_bonuses(self) -> Abilities:
        # getting one of variable ability bonus for specific npc
        const_ability_bonus = Abilities.init_with_const(
            self.race.const_ability_bonus.all(),
            value=2,
        )
        if self.var_bonus_ability:
            var_ability_bonus = Abilities.init_with_const(
                Ability.objects.filter(title=self.var_bonus_ability.title), value=2
            )
        else:
            var_ability_bonus = Abilities()
        return const_ability_bonus + var_ability_bonus

    @property
    def _level_abilities_bonuses(self) -> Abilities:
        query = (
            AbilityLevelBonus.objects.filter(npc=self)
            .values_list(Lower('ability__title'))
            .annotate(bonus=models.Count('ability__title'))
        )
        bonuses = {item[0]: item[1] for item in query}
        return Abilities(**bonuses)

    @property
    def _tier_attrs_bonus(self) -> Abilities:
        return Abilities.init_with_const(Ability.objects.all(), value=self._tier)

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
