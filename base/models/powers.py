import operator
import re
from itertools import chain
from typing import Sequence

from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    AccessoryTypeEnum,
    DefenceTypeEnum,
    DiceIntEnum,
    NPCClassEnum,
    NPCOtherProperties,
    PowerActionTypeEnum,
    PowerDamageTypeEnum,
    PowerEffectTypeEnum,
    PowerFrequencyIntEnum,
    PowerPropertyTitle,
    PowerRangeTypeEnum,
    PowerVariables,
)
from base.exceptions import PowerInconsistent
from base.models.abilities import Ability
from base.models.books import BookSource
from base.models.items import ItemAbstract, Weapon
from base.models.npc_protocol import NPCProtocol
from base.objects.dice import DiceRoll
from base.objects.powers_output import PowerDisplay, PowerPropertyDisplay


class Effect(models.Model):
    class Meta:
        verbose_name = _('Effect type')
        verbose_name_plural = _('Effect types')

    name = models.CharField(
        verbose_name=_('Name'),
        choices=chain(
            PowerDamageTypeEnum.generate_choices(),
            PowerEffectTypeEnum.generate_choices(
                condition=lambda x: x != PowerEffectTypeEnum.NONE
            ),
        ),
        max_length=max(
            (PowerEffectTypeEnum.max_length(), PowerDamageTypeEnum.max_length())
        ),
        unique=True,
    )
    is_damage = models.BooleanField(
        verbose_name=_('Is damage?'),
        help_text=_('Shows if damage can have this effect'),
        default=False,
    )

    def __str__(self) -> str:
        return self.get_name_display()


class Power(models.Model):
    class Meta:
        verbose_name = _('Power')
        verbose_name_plural = _('Powers')

    name = models.CharField(verbose_name=_('Title'), max_length=100)
    description = models.TextField(
        verbose_name=_('Description'), default='', blank=True
    )
    frequency = models.PositiveSmallIntegerField(
        verbose_name=_('Usage frequency'),
        choices=PowerFrequencyIntEnum.generate_choices(),
        default=PowerFrequencyIntEnum.PASSIVE.value,
    )
    action_type = models.CharField(
        verbose_name=_('Action type'),
        choices=PowerActionTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerActionTypeEnum.max_length(),
        default=PowerActionTypeEnum.STANDARD.value,
        null=True,
        blank=False,
        help_text=_('Choose, if power frequency is not passive'),
    )
    klass = models.ForeignKey(
        'base.Class',
        related_name='powers',
        verbose_name=_('Class'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    subclass = models.ForeignKey(
        'base.Subclass',
        related_name='powers',
        verbose_name=_('Subclass'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    race = models.ForeignKey(
        'base.Race',
        verbose_name=_('Race'),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name='powers',
    )
    functional_template = models.ForeignKey(
        'base.FunctionalTemplate',
        verbose_name=_('Functional template'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='powers',
    )
    paragon_path = models.ForeignKey(
        'base.ParagonPath',
        verbose_name=_('Paragon path'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='powers',
    )
    magic_item_type = models.ForeignKey(
        'MagicItemType',
        verbose_name=_('Magic item type'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='powers',
    )
    skill = models.ForeignKey(
        'base.Skill',
        verbose_name=_('Skill'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='powers',
    )
    level = models.SmallIntegerField(verbose_name=_('Level'), default=0)
    attack_ability = models.ForeignKey(
        Ability,
        verbose_name=_('Attack ability'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    attack_bonus = models.SmallIntegerField(verbose_name=_('Attack bonus'), default=0)
    defence = models.CharField(
        verbose_name=_('against'),
        choices=DefenceTypeEnum.generate_choices(is_sorted=False),
        max_length=DefenceTypeEnum.max_length(),
        help_text=_('defence'),
        null=True,
        blank=True,
    )
    damage_types = models.ManyToManyField(
        Effect,
        verbose_name=_('Damage type'),
        blank=True,
        limit_choices_to={'is_damage': True},
        related_name='powers',
    )
    effects = models.ManyToManyField(
        Effect,
        verbose_name=_('Effects'),
        blank=True,
        limit_choices_to={'is_damage': False},
    )
    dice_number = models.SmallIntegerField(verbose_name=_('Dice number'), default=1)
    damage_dice = models.SmallIntegerField(
        verbose_name=_('Damage dice'),
        choices=DiceIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    accessory_type = models.CharField(
        verbose_name=_('Accessory type'),
        choices=AccessoryTypeEnum.generate_choices(),
        max_length=AccessoryTypeEnum.max_length(),
        null=True,
        blank=True,
    )
    weapon_types = models.ManyToManyField(
        'base.WeaponType',
        verbose_name=_('Weapon requirement'),
        help_text=_('for powers with weapons'),
        blank=True,
    )
    range_type = models.CharField(
        verbose_name=_('Range type'),
        choices=PowerRangeTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerRangeTypeEnum.max_length(),
        default=PowerRangeTypeEnum.PERSONAL.value,
    )
    range = models.SmallIntegerField(verbose_name=_('Distance'), default=0)
    burst = models.SmallIntegerField(verbose_name=_('Area'), default=0)
    book_source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.race:
            return f'{self.name}, ({self.race}), {self.level} уровень'
        if self.functional_template:
            return f'{self.name}, ({self.functional_template})'
        if self.klass:
            return (
                f'{self.name}, '
                f'{self.klass} '
                f'({(str(self.attack_ability) if self.attack_ability else "Пр")[:3]}), '
                f'{self.get_frequency_display()}, '
                f'{self.level} уровень'
            )
        if self.magic_item_type:
            return f'{self.name} - {self.magic_item_type}'
        if self.paragon_path:
            return f'{self.name}, ({self.paragon_path}), {self.level} уровень'
        if self.skill:
            return f'{self.name}, ({self.skill}), {self.level} уровень'
        return self.name

    @property
    def defence_subjanctive(self):
        # defence subjanctive case for Russian language
        if self.defence == DefenceTypeEnum.ARMOR_CLASS:
            return self.get_defence_display()
        return self.get_defence_display()[:-1] + 'и'

    @property
    def damage(self):
        return f'{self.dice_number}{self.get_damage_dice_display()}'

    def category(
        self,
        weapons: Sequence["Weapon"] = (),
    ):
        # TODO localization
        if self.magic_item_type:
            return self.magic_item_type.name
        result = []
        try:
            if self.functional_template:
                result.append(self.functional_template.title)
            if self.paragon_path:
                result.append(self.paragon_path.title)
            if self.race:
                result.append(str(self.race))
            if self.klass:
                result.append(str(self.klass))
            if self.accessory_type in (
                AccessoryTypeEnum.WEAPON,
                AccessoryTypeEnum.IMPLEMENT,
            ):
                result.append(str(weapons[0]))
            if self.accessory_type == AccessoryTypeEnum.TWO_WEAPONS:
                result.extend(map(str, weapons))
            if self.level % 2 == 0 and self.level > 0:
                result.append('Приём')
            if self.frequency == PowerFrequencyIntEnum.PASSIVE:
                result.append('Пассивный')
        except (TypeError, IndexError, ValueError) as e:
            raise PowerInconsistent(f'Power {self} is improperly configured: {e}')
        if not result:
            raise PowerInconsistent(f'Power {self} is improperly configured')
        return '; '.join(result)

    @property
    def default_target(self):
        if self.range_type in (
            PowerRangeTypeEnum.MELEE_WEAPON,
            PowerRangeTypeEnum.MELEE,
            PowerRangeTypeEnum.RANGED,
            PowerRangeTypeEnum.MELEE_RANGED_WEAPON,
            PowerRangeTypeEnum.RANGED_WEAPON,
        ):
            return 'Одно существо'
        if self.range_type == PowerRangeTypeEnum.BURST:
            return 'Все существа во вспышке'
        if self.range_type == PowerRangeTypeEnum.BLAST:
            return 'Все существа в волне'
        return '----------'

    def attack_type(self, weapon=None) -> str:
        if (
            self.range_type
            in (
                PowerRangeTypeEnum.MELEE_RANGED_WEAPON,
                PowerRangeTypeEnum.MELEE_WEAPON,
                PowerRangeTypeEnum.RANGED_WEAPON,
            )
            and weapon
        ):
            return weapon.get_attack_type(
                is_melee=self.range_type
                in (
                    PowerRangeTypeEnum.MELEE_WEAPON,
                    PowerRangeTypeEnum.MELEE_RANGED_WEAPON,
                ),
                is_ranged=self.range_type
                in (
                    PowerRangeTypeEnum.RANGED_WEAPON,
                    PowerRangeTypeEnum.MELEE_RANGED_WEAPON,
                ),
            )

        if self.range_type == PowerRangeTypeEnum.PERSONAL:
            return self.get_range_type_display()
        if (
            self.range_type
            in (
                PowerRangeTypeEnum.MELEE,
                PowerRangeTypeEnum.RANGED,
            )
            and self.range
        ):
            return f'{self.get_range_type_display().split()[0]} {self.range}'
        if self.range_type == PowerRangeTypeEnum.MELEE:
            return f'{self.get_range_type_display()} касание'
        if self.range_type == PowerRangeTypeEnum.RANGED:
            return f'{self.get_range_type_display()} видимость'
        if (
            self.range_type
            in (
                PowerRangeTypeEnum.BURST,
                PowerRangeTypeEnum.BLAST,
            )
            and not self.range
        ):
            return f'Ближняя {self.get_range_type_display().lower()} {self.burst}'
        if self.range_type in (
            PowerRangeTypeEnum.BURST,
            PowerRangeTypeEnum.WALL,
        ):
            return (
                f'Зональная {self.get_range_type_display().lower()} '
                f'{self.burst} в пределах {self.range}'
            )
        raise PowerInconsistent(_('Wrong attack type'))

    def keywords(self, weapons: Sequence["Weapon"] = ()) -> str:
        if self.frequency == PowerFrequencyIntEnum.PASSIVE:
            return ''
        return ', '.join(
            filter(
                None,
                (
                    self.get_action_type_display(),
                    self.get_accessory_type_display() if self.accessory_type else '',
                    self.get_frequency_display(),
                )
                + tuple(self.attack_type(weapon) for weapon in weapons if weapon)
                + tuple(
                    str(damage_type)
                    for damage_type in self.damage_types.exclude(
                        name=PowerDamageTypeEnum.UNTYPED
                    )
                )
                + tuple(str(effect) for effect in self.effects.all()),
            )
        )

    @property
    def text(self) -> str:
        result = []
        if self.description:
            result.append(self.description)
        for prop in self.properties.all():
            if not prop.title or prop.title == PowerPropertyTitle.OTHER:
                title, description = prop.description.split(':')
            else:
                title = PowerPropertyTitle[prop.title].description
                description = prop.description
            result.append(f'{title}: {description}')
        return '\n'.join(result)


class PowerProperty(models.Model):
    class Meta:
        verbose_name = _('Power Property')
        verbose_name_plural = _('Power Properties')

    power = models.ForeignKey(
        Power,
        verbose_name=_('Power'),
        null=False,
        on_delete=models.CASCADE,
        related_name='properties',
    )
    title = models.CharField(
        choices=PowerPropertyTitle.generate_choices(),
        null=True,
        blank=True,
        max_length=PowerPropertyTitle.max_length(),
    )
    level = models.SmallIntegerField(verbose_name=_('Level'), default=1)
    subclass = models.SmallIntegerField(
        verbose_name=_('Subclass'),
        default=0,
    )
    description = models.TextField(
        verbose_name=_('Description'), blank=True, default=''
    )
    order = models.SmallIntegerField(verbose_name=_('Order'), default=0)

    def get_displayed_title(self):
        if self.title and self.title != PowerPropertyTitle.OTHER:
            return self.get_title_display()
        return self.description.split(':')[0]

    def get_displayed_description(self):
        if self.title and self.title != PowerPropertyTitle.OTHER:
            return self.description
        return ':'.join(self.description.split(':')[1:])

    def __str__(self):
        return f'{self.title} {self.description} {self.level}'


class PowerMixin:
    OPERATORS = {
        '+': (operator.add, 0),
        '-': (operator.sub, 0),
        '*': (operator.mul, 1),
        '/': (operator.floordiv, 1),
        '^': (max, 2),
        '_': (min, 2),
    }

    @property
    def _power_attrs(self: NPCProtocol):
        return {
            PowerVariables.STR: self.str_mod,
            PowerVariables.CON: self.con_mod,
            PowerVariables.DEX: self.dex_mod,
            PowerVariables.INT: self.int_mod,
            PowerVariables.WIS: self.wis_mod,
            PowerVariables.CHA: self.cha_mod,
            PowerVariables.LVL: self.level,
        }

    @property
    def _is_no_hand_implement_ki_focus(self: NPCProtocol) -> bool:
        if not self.no_hand:
            return False
        return self.no_hand.weapon_type.slug == 'KiFocus'

    def _can_get_bonus_from_implement_to_weapon(
        self: NPCProtocol, accessory_type: AccessoryTypeEnum | None
    ):
        return (
            self._is_no_hand_implement_ki_focus
            and self.is_implement_proficient(self.no_hand)
            and accessory_type
            in (AccessoryTypeEnum.WEAPON, AccessoryTypeEnum.TWO_WEAPONS)
        )

    def _calculate_weapon_damage(
        self: NPCProtocol, weapon: "Weapon", accessory_type: AccessoryTypeEnum | None
    ):
        if not weapon:
            # TODO deal with error message
            raise PowerInconsistent(_("This power doesn't use weapon"))
        damage_roll = weapon.damage_roll
        if self._can_get_bonus_from_implement_to_weapon(accessory_type):
            damage_roll.addendant = max(damage_roll.addendant, self.no_hand.enhancement)
        return damage_roll.threshold(self._magic_threshold)

    def attack_bonus(self: NPCProtocol, weapon=None, is_implement: bool = False) -> int:
        result = self._level_bonus + self.half_level
        if weapon and not is_implement and self.is_weapon_proficient(weapon=weapon):
            result += weapon.prof_bonus
        if self.klass.name == NPCClassEnum.FIGHTER and weapon:
            if self.subclass.slug == 'GREAT_WEAPON':
                if (
                    not self.shield
                    and weapon.handedness.is_two_handed
                    and bool(self.primary_hand) != bool(self.secondary_hand)  # xor
                ):
                    result += 1
            if self.subclass.slug == 'GUARDIAN':
                if weapon.handedness.is_one_handed:
                    return result + 1
            if self.subclass.slug == 'TEMPPEST':
                if (
                    self.primary_hand
                    and self.secondary_hand
                    and weapon.handedness.is_off_hand
                ):
                    return result + 1

        if (
            self.klass.name == NPCClassEnum.SEEKER
            and self.subclass == 'SPIRITBOND'
            and weapon.weapon_type.thrown
        ):
            result += 1

        if (
            self.klass.name == NPCClassEnum.ROGUE
            and weapon
            and (
                weapon.weapon_type in self.klass.weapon_types.all()
                or weapon.weapon_type in self.subclass.weapon_types.all()
                and weapon.weapon_type.slug in ('Dagger', 'Sling', 'HandCrossbow')
            )
        ):  # TODO handle rogue subclasses for it
            result += 1
        return result

    def _calculate_attack(
        self: NPCProtocol, weapon: "Weapon", accessory_type: AccessoryTypeEnum | None
    ):
        if not weapon:
            return self.attack_bonus()
        enhancement = weapon.enhancement
        if self._can_get_bonus_from_implement_to_weapon(accessory_type):
            enhancement = max(enhancement, self.no_hand.enhancement)
        return (
            self.attack_bonus(
                weapon, is_implement=accessory_type == AccessoryTypeEnum.IMPLEMENT
            )
            # armament enchantment
            + self.enhancement_with_magic_threshold(enhancement)
            # power attack bonus will be added to power string
            # during the power property creation
        )

    def _calculate_damage_bonus(
        self: NPCProtocol, weapon: "Weapon", accessory_type: AccessoryTypeEnum | None
    ):
        enhancement = weapon and weapon.enhancement or 0
        if self._can_get_bonus_from_implement_to_weapon(accessory_type):
            enhancement = max(enhancement, self.no_hand.enhancement)
        return (
            self.damage_bonus
            + self.calculate_bonus(NPCOtherProperties.DAMAGE)
            + self.enhancement_with_magic_threshold(enhancement)
        )

    def calculate_token(
        self: NPCProtocol,
        token: str,
        accessory_type: AccessoryTypeEnum | None,
        weapon=None,
        secondary_weapon=None,
        item=None,
    ) -> int | DiceRoll:
        if token.isdigit():
            return int(token)
        if token == PowerVariables.WPN:
            return self._calculate_weapon_damage(weapon, accessory_type)
        if token == PowerVariables.WPS:
            return self._calculate_weapon_damage(secondary_weapon, accessory_type)
        if token == PowerVariables.ATK:
            return self._calculate_attack(
                weapon,
                accessory_type,
            )
        if token == PowerVariables.ATS:
            return self._calculate_attack(
                secondary_weapon,
                accessory_type,
            )
        if token == PowerVariables.DMG:
            return self._calculate_damage_bonus(weapon, accessory_type)
        if token == PowerVariables.DMS:
            return self._calculate_damage_bonus(secondary_weapon, accessory_type)
        if token == PowerVariables.EHT:
            return self.enhancement_with_magic_threshold(
                weapon and weapon.enhancement or 0
            )
        if token == PowerVariables.EHS:
            return self.enhancement_with_magic_threshold(
                secondary_weapon and secondary_weapon.enhancement or 0
            )
        if token == PowerVariables.ITL:
            if not item:
                raise PowerInconsistent(_("This power doesn't use magic item"))
            return item.level
        if token in self._power_attrs:
            return self._power_attrs[token]
        return DiceRoll.from_str(token)

    def enhancement_with_magic_threshold(self: NPCProtocol, enhancement: int) -> int:
        return max((0, enhancement - self._magic_threshold))

    def calculate_reverse_polish_notation(
        self: NPCProtocol,
        expression: str,
        accessory_type: AccessoryTypeEnum | None,
        weapon=None,
        secondary_weapon=None,
        item=None,
    ):
        """
        Проходим постфиксную запись;
        При нахождении числа, парсим его и заносим в стек;
        При нахождении бинарного оператора,
        берём два последних значения из стека в обратном порядке;
        Последнее значение, после отработки алгоритма, является решением выражения.
        """
        stack: list[str | int | DiceRoll] = []
        for token in expression.split():
            if token in self.OPERATORS:
                right, left = stack.pop(), stack.pop()
                stack.append(self.OPERATORS[token][0](left, right))  # type: ignore
            else:
                stack.append(
                    self.calculate_token(
                        token, accessory_type, weapon, secondary_weapon, item
                    )
                )
        return stack.pop()

    @classmethod
    def expression_to_reverse_polish_notation(cls, string: str) -> str:
        """
        Пока не все токены обработаны:

        Прочитать токен.
        Если токен — число, то добавить его в очередь вывода.
        Если токен — оператор op1, то:
            Пока присутствует на вершине стека токен оператор op2,
                    чей приоритет выше или равен приоритету op1,
                    и при равенстве приоритетов op1 является левоассоциативным:
                Переложить op2 из стека в выходную очередь;
            Положить op1 в стек.

        Если токен — открывающая скобка, то положить его в стек.
        Если токен — закрывающая скобка:
            Пока токен на вершине стека не открывающая скобка
                Переложить оператор из стека в выходную очередь.
                Если стек закончился до того,
                    как был встречен токен открывающая скобка,
                    то в выражении пропущена скобка.
            Выкинуть открывающую скобку из стека, но не добавлять в очередь вывода.
            Если токен на вершине стека — функция, переложить её в выходную очередь.

        Если больше не осталось токенов на входе:
            Пока есть токены операторы в стеке:
                Если токен оператор на вершине стека — открывающая скобка,
                    то в выражении пропущена скобка.
                Переложить оператор из стека в выходную очередь.
        Конец.
        """
        stack = []
        result = []
        operand: list[str] = []
        for char in string:
            if char in cls.OPERATORS or char in ('(', ')'):
                if operand:
                    result.append(''.join(operand))
                    operand = []
            if char == '(':
                stack.append(char)
            elif char in cls.OPERATORS:
                priority = cls.OPERATORS[char][1]
                while stack and stack[-1] in cls.OPERATORS:
                    if cls.OPERATORS[stack[-1]][1] >= priority:
                        result.append(stack.pop())
                    else:
                        break
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()
            else:
                operand.append(char)
        if operand:
            result.append(''.join(operand))

        while stack:
            result.append(stack.pop())
        return ' '.join(result)

    def evaluate_power_expression(
        self: NPCProtocol,
        string: str,
        accessory_type: AccessoryTypeEnum | None = None,
        weapon=None,
        secondary_weapon=None,
        item=None,
    ):
        return self.calculate_reverse_polish_notation(
            self.expression_to_reverse_polish_notation(string),
            accessory_type,
            weapon,
            secondary_weapon,
            item,
        )

    def valid_properties(self: NPCProtocol, power: Power):
        """collecting power properties,
        replacing properties without subclass with subclassed properties
        and properties with lower level with properties with high level
        should they appeared
        """
        properties: dict[str, PowerProperty] = {}
        for prop in power.properties.filter(
            level__lte=self.level, subclass__in=(self.subclass_id, 0)  # type: ignore
        ).order_by('-subclass'):
            key = f'{prop.get_displayed_title()},{prop.order}'
            if key not in properties or properties[key].level < prop.level:
                properties[key] = prop
        return sorted(properties.values(), key=lambda x: x and x.order)

    @staticmethod
    def get_power_inconsistent_message(power: Power):
        message = 'POWER INCONSISTENT'
        return PowerDisplay(
            name=power.name,
            keywords=message,
            category=message,
            description=message,
            frequency_order=0,
            frequency_css_class=PowerFrequencyIntEnum.PASSIVE.name,
            frequency=message,
            properties=[],
        ).asdict()

    def parse_string(
        self: NPCProtocol,
        accessory_type: AccessoryTypeEnum | None,
        string: str,
        weapons: Sequence["Weapon"] = (),
        item: ItemAbstract | None = None,
    ):
        try:
            primaty_weapon = weapons[0] or weapons[2]
        except (TypeError, IndexError):
            primaty_weapon = None
        try:
            secondary_weapon = weapons[1]
        except (TypeError, IndexError):
            secondary_weapon = None
        pattern = r'\$(\S+)\b'  # gets substring from '$' to next whitespace
        # TODO fix parsing cases with ")" as a last character.
        #  Now it's unmatched by regexp
        expressions_to_calculate = re.findall(pattern, string)
        template = re.sub(
            pattern, '{}', string
        )  # preparing template for format() method
        calculated_expressions = []
        for expression in expressions_to_calculate:
            calculated_expressions.append(
                self.evaluate_power_expression(
                    string=expression,
                    accessory_type=accessory_type,
                    weapon=primaty_weapon,
                    secondary_weapon=secondary_weapon,
                    item=item,
                )
            )
        return template.format(*calculated_expressions)

    def get_power_display(
        self: NPCProtocol,
        *,
        power: Power,
        weapons: Sequence["Weapon"] = (),
        item: ItemAbstract | None = None,
    ) -> dict[str, str]:
        return PowerDisplay(
            name=power.name,
            keywords=power.keywords(weapons),
            category=power.category(weapons),
            description=self.parse_string(
                accessory_type=(
                    AccessoryTypeEnum[power.accessory_type]
                    if power.accessory_type
                    else None
                ),
                string=power.description,
                weapons=weapons,
                item=item,
            ),
            frequency_order=power.frequency,  # type: ignore
            frequency_css_class=PowerFrequencyIntEnum(power.frequency).name.lower(),
            frequency=power.get_frequency_display(),
            properties=[
                PowerPropertyDisplay(
                    title=prop.get_displayed_title(),
                    description=self.parse_string(
                        (
                            AccessoryTypeEnum[power.accessory_type]
                            if power.accessory_type
                            else None
                        ),
                        string=prop.get_displayed_description(),
                        weapons=weapons,
                        item=item,
                    ),
                    debug=prop.get_displayed_description(),
                )
                for prop in self.valid_properties(power)
            ],
        ).asdict()

    def magic_item_powers(self: NPCProtocol) -> models.QuerySet[Power]:
        return Power.objects.filter(
            frequency=PowerFrequencyIntEnum.PASSIVE,
            magic_item_type__in=(mi.magic_item_type for mi in self.magic_items),
        )

    @property
    def _powers_cache_key(self: NPCProtocol) -> str:
        return f'npc-{self.id}-powers'

    def cache_powers(self: NPCProtocol):
        cache.set(self._powers_cache_key, self.powers_calculate())
