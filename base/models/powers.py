import operator

from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import (
    AbilityEnum,
    AccessoryTypeEnum,
    DefenceTypeEnum,
    DiceIntEnum,
    PowerActionTypeEnum,
    PowerDamageTypeEnum,
    PowerEffectTypeEnum,
    PowerFrequencyEnum,
    PowerPropertyTitle,
    PowerRangeTypeEnum,
    PowerVariables,
)
from base.exceptions import PowerInconsistent
from base.managers import PowerQueryset
from base.models.bonuses import Bonus
from base.objects.dice import DiceRoll
from base.objects.npc_classes import NPCClass


class Power(models.Model):
    class Meta:
        verbose_name = _('Power')
        verbose_name_plural = _('Powers')

    objects = PowerQueryset.as_manager()

    name = models.CharField(verbose_name=_('Title'), max_length=100)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    frequency = models.CharField(
        verbose_name=_('Usage frequency'),
        choices=PowerFrequencyEnum.generate_choices(is_sorted=False),
        max_length=PowerFrequencyEnum.max_length(),
    )
    action_type = models.CharField(
        verbose_name=_('Action type'),
        choices=PowerActionTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerActionTypeEnum.max_length(),
        default=PowerActionTypeEnum.STANDARD,
        null=True,
        blank=False,
    )
    klass = models.ForeignKey(
        'base.Class',
        related_name='powers',
        verbose_name=_('Class'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    subclass = models.SmallIntegerField(
        verbose_name=_('Subclass'),
        default=0,
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
    level = models.SmallIntegerField(verbose_name=_('Level'), default=0)
    attack_ability = models.CharField(
        verbose_name=_('Attack ability'),
        choices=AbilityEnum.generate_choices(is_sorted=False),
        max_length=AbilityEnum.max_length(),
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
    effect_type = MultiSelectField(
        verbose_name=_('Effect type'),
        choices=PowerEffectTypeEnum.generate_choices(),
        default=PowerEffectTypeEnum.NONE,
    )
    damage_type = MultiSelectField(
        verbose_name=_('Damage type'),
        choices=PowerDamageTypeEnum.generate_choices(),
        default=PowerDamageTypeEnum.NONE,
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
    available_weapon_types = models.ManyToManyField(
        'base.WeaponType',
        verbose_name=_('Weapon requirement'),
        help_text=_('for powers with weapons'),
        blank=True,
    )
    range_type = models.CharField(
        verbose_name=_('Range type'),
        choices=PowerRangeTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerRangeTypeEnum.max_length(),
        default=PowerRangeTypeEnum.PERSONAL,
    )
    range = models.SmallIntegerField(verbose_name=_('Distance'), default=0)
    burst = models.SmallIntegerField(verbose_name=_('Area'), default=0)

    bonus = models.ForeignKey(
        Bonus, verbose_name=_('Bonus'), null=True, on_delete=models.SET_NULL, blank=True
    )

    def __str__(self):
        if self.race:
            return f'{self.name}, {self.race.get_name_display()}'
        if self.functional_template:
            return f'{self.name}, {self.functional_template}'
        if self.klass:
            return (
                f'{self.name}, '
                f'{self.klass.get_name_display()} '
                f'({(self.get_attack_ability_display() or "Пр")[:3]}), '
                f'{self.get_frequency_display()}, '
                f'{self.level} уровень'
            )
        if self.magic_item_type:
            return f'{self.name} - {self.magic_item_type}'
        if self.paragon_path:
            return f'{self.name}, {self.paragon_path}'
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
        primary_weapon=None,
        secondary_weapon=None,
    ):
        # TODO localization
        if self.magic_item_type:
            return self.magic_item_type.name
        if self.functional_template:
            return self.functional_template.title
        if self.paragon_path:
            return self.paragon_path.title
        if self.race:
            return self.race.get_name_display()
        if self.accessory_type in (
            AccessoryTypeEnum.WEAPON,
            AccessoryTypeEnum.IMPLEMENT,
        ):
            return str(primary_weapon)
        if self.accessory_type == AccessoryTypeEnum.TWO_WEAPONS:
            return f'{primary_weapon}, {secondary_weapon}'
        if self.level % 2 == 0 and self.level > 0:
            return 'Приём'
        if self.frequency == PowerFrequencyEnum.PASSIVE:
            return 'Пассивный'
        if self.klass:
            return self.klass.get_name_display()
        raise ValueError('Power improperly configured')

    def attack_type(self, weapon=None):
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

    def keywords(self, weapon=None):
        if self.frequency == PowerFrequencyEnum.PASSIVE:
            return ''
        return filter(
            None,
            (
                self.get_action_type_display(),
                self.get_accessory_type_display() if self.accessory_type else '',
                self.get_frequency_display(),
                self.attack_type(weapon),
            )
            + tuple(
                PowerDamageTypeEnum[type_].description  # type: ignore
                for type_ in self.damage_type
                if type_ != PowerDamageTypeEnum.NONE
            )
            + tuple(
                PowerEffectTypeEnum[type_].description  # type: ignore
                for type_ in self.effect_type
                if type_ != PowerEffectTypeEnum.NONE
            ),
        )

    @property
    def text(self) -> str:
        result = []
        if self.description:
            result.append(self.description)
        for prop in self.properties.all():
            if prop.title == PowerPropertyTitle.OTHER:
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
        choices=IntDescriptionSubclassEnum.generate_choices(),
        default=0,
    )
    description = models.TextField(verbose_name=('Description'), blank=True, null=True)
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

    klass_data_instance: NPCClass
    _magic_threshold: int

    @property
    def _power_attrs(self):
        return {
            PowerVariables.STR: self.str_mod,
            PowerVariables.CON: self.con_mod,
            PowerVariables.DEX: self.dex_mod,
            PowerVariables.INT: self.int_mod,
            PowerVariables.WIS: self.wis_mod,
            PowerVariables.CHA: self.cha_mod,
            PowerVariables.LVL: self.level,
        }

    def calculate_token(
        self, token: str, power, weapon=None, secondary_weapon=None, item=None
    ) -> int | DiceRoll:
        if token.isdigit():
            return int(token)
        if token == PowerVariables.WPN:
            weapon = weapon or self.primary_hand  # type: ignore
            if not weapon:
                raise PowerInconsistent(_("This power doesn't use weapon"))
            return weapon.damage_roll.treshhold(self._magic_threshold)
        if token == PowerVariables.WPS:
            if not secondary_weapon:
                raise PowerInconsistent(_("This power doesn't use off-hand weapon"))
            return secondary_weapon.damage_roll.treshhold(self._magic_threshold)
        if token == PowerVariables.ATK:
            return (
                self.klass_data_instance.attack_bonus(
                    weapon,
                    is_implement=power.accessory_type == AccessoryTypeEnum.IMPLEMENT,
                )
                # armament enchantment
                + self.enhancement_with_magic_threshold(
                    weapon and weapon.enchantment or 0
                )
                # power attack bonus will be added to power string
                # during the power property creation
            )
        if token == PowerVariables.DMG:
            return (
                self.klass_data_instance.damage_bonus
                + self.enhancement_with_magic_threshold(
                    weapon and weapon.enchantment or 0
                )
            )
        if token == PowerVariables.EHT:
            return self.enhancement_with_magic_threshold(
                weapon and weapon.enchantment or 0
            )
        if token == PowerVariables.ITL:
            if not item:
                raise PowerInconsistent(_("This power doesn't use magic item"))
            return item.level
        if token in self._power_attrs:
            return self._power_attrs[token]
        return DiceRoll.from_str(token)

    def enhancement_with_magic_threshold(self, enhancement: int) -> int:
        return max((0, enhancement - self._magic_threshold))

    def calculate_reverse_polish_notation(
        self, expression: str, power, weapon=None, secondary_weapon=None, item=None
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
                    self.calculate_token(token, power, weapon, secondary_weapon, item)
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
        self, string: str, power=None, weapon=None, secondary_weapon=None, item=None
    ):
        return self.calculate_reverse_polish_notation(
            self.expression_to_reverse_polish_notation(string),
            power,
            weapon,
            secondary_weapon,
            item,
        )

    def valid_properties(self, power: Power):
        """collecting power properties,
        replacing properties without subclass with subclassed properties
        and properties with lower level with properties with high level
        should they appeared
        """
        properties: dict[str, PowerProperty] = {}
        for prop in power.properties.filter(
            level__lte=self.level, subclass__in=(self.subclass, 0)  # type: ignore
        ).order_by('-subclass'):
            key = f'{prop.get_displayed_title()},{prop.order}'
            if key not in properties or properties[key].level < prop.level:
                properties[key] = prop
        return sorted(properties.values(), key=lambda x: x and x.order)
