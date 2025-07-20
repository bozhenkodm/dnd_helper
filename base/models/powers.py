import operator
import re
from itertools import chain
from typing import Sequence

from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from pytesseract import image_to_string

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
from base.models.klass import Class
from base.models.npc_protocol import NPCProtocol
from base.objects.dice import DiceRoll
from base.objects.powers_output import PowerDisplay, PowerPropertyDisplay


class Effect(models.Model):
    """Represents special effects and damage types that can be applied to powers.

    Effects can be either damage types (fire, cold, necrotic, etc.) or
    special conditions (prone, dazed, stunned, etc.) that powers can inflict.
    Used to categorize and filter power effects in the admin interface.
    """

    class Meta:
        verbose_name = _('Effect type')
        verbose_name_plural = _('Effect types')

    # Combined choices from damage types and effect types (excluding NONE)
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
    # Flag to distinguish between damage types and condition effects
    is_damage = models.BooleanField(
        verbose_name=_('Is damage?'),
        help_text=_('Shows if damage can have this effect'),
        default=False,
    )

    def __str__(self) -> str:
        return self.get_name_display()


class Power(models.Model):
    """Represents a D&D 4th Edition power (spell, ability, or special action).

    Powers can belong to classes, races,
    paragon paths, magic items, or functional templates.
    Each power has usage frequency, action type, range, damage, and special properties.
    Powers use a sophisticated expression system
    for dynamic calculation of attack rolls,
    damage rolls, and other numeric values based on character statistics.
    """

    class Meta:
        verbose_name = _('Power')
        verbose_name_plural = _('Powers')

    name = models.CharField(verbose_name=_('Title'), max_length=100)
    description = models.TextField(
        verbose_name=_('Description'), default='', blank=True
    )

    # How often the power can be used (at-will, encounter, daily, passive)
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
    # === POWER SOURCE RELATIONSHIPS ===
    # Only one of these should be set per power to indicate the source

    # Class-based power (e.g., Fighter, Wizard powers)
    klass = models.ForeignKey(
        'base.Class',
        related_name='powers',
        verbose_name=_('Class'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # Subclass-specific power (e.g., Guardian Fighter, Great Weapon Fighter)
    subclass = models.ForeignKey(
        'base.Subclass',
        related_name='powers',
        verbose_name=_('Subclass'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'subclass_id__gt': 0},
    )
    # Racial power (e.g., Dragonborn Breath, Dwarf Second Wind)
    race = models.ForeignKey(
        'base.Race',
        verbose_name=_('Race'),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name='powers',
    )
    # Functional template power (e.g., Lurker, Soldier template abilities)
    functional_template = models.ForeignKey(
        'base.FunctionalTemplate',
        verbose_name=_('Functional template'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='powers',
    )
    # Paragon path power (level 11+ advancement path)
    paragon_path = models.ForeignKey(
        'base.ParagonPath',
        verbose_name=_('Paragon path'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='powers',
    )
    # Magic item power (granted by equipped magical items)
    magic_item_type = models.ForeignKey(
        'base.MagicItemType',
        verbose_name=_('Magic item type'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='powers',
    )
    # Skill-based power (utility powers based on trained skills)
    skill = models.ForeignKey(
        'base.Skill',
        verbose_name=_('Skill'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='powers',
    )

    # Minimum level required to use this power
    level = models.SmallIntegerField(verbose_name=_('Level'), default=0)
    # Which ability modifier is used for attack rolls (STR, DEX, etc.)
    attack_ability = models.ForeignKey(
        Ability,
        verbose_name=_('Attack ability'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # Fixed bonus added to attack rolls
    attack_bonus = models.SmallIntegerField(verbose_name=_('Attack bonus'), default=0)
    # Which defense the attack targets (AC, Fortitude, Reflex, Will)
    defence = models.CharField(
        verbose_name=_('against'),
        choices=DefenceTypeEnum.generate_choices(is_sorted=False),
        max_length=DefenceTypeEnum.max_length(),
        help_text=_('defence'),
        null=True,
        blank=True,
    )

    # Types of damage this power deals (fire, cold, necrotic, etc.)
    damage_types = models.ManyToManyField(
        Effect,
        verbose_name=_('Damage type'),
        blank=True,
        limit_choices_to={'is_damage': True},
        related_name='powers',
    )
    # Special effects this power can inflict (prone, dazed, etc.)
    effects = models.ManyToManyField(
        Effect,
        verbose_name=_('Effects'),
        blank=True,
        limit_choices_to={'is_damage': False},
    )

    # Number of dice to roll (e.g., 2 in "2d6")
    dice_number = models.SmallIntegerField(verbose_name=_('Dice number'), default=1)
    # Type of dice to roll (e.g., 6 in "2d6")
    damage_dice = models.SmallIntegerField(
        verbose_name=_('Damage dice'),
        choices=DiceIntEnum.generate_choices(),
        null=True,
        blank=True,
    )

    # What type of equipment is required (weapon, implement, two weapons)
    accessory_type = models.CharField(
        verbose_name=_('Accessory type'),
        choices=AccessoryTypeEnum.generate_choices(),
        max_length=AccessoryTypeEnum.max_length(),
        null=True,
        blank=True,
    )
    # Specific weapon types required for this power
    weapon_types = models.ManyToManyField(
        'base.WeaponType',
        verbose_name=_('Weapon requirement'),
        help_text=_('for powers with weapons'),
        blank=True,
    )

    # Type of attack range (melee, ranged, burst, blast, etc.)
    range_type = models.CharField(
        verbose_name=_('Range type'),
        choices=PowerRangeTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerRangeTypeEnum.max_length(),
        default=PowerRangeTypeEnum.PERSONAL.value,
    )
    # Maximum range in squares (0 for touch/weapon reach)
    range = models.SmallIntegerField(verbose_name=_('Distance'), default=0)
    # Size of area effect (burst/blast radius)
    burst = models.SmallIntegerField(verbose_name=_('Area'), default=0)

    # Reference to the D&D sourcebook where this power is defined
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
        if weapons:
            range_type = tuple(self.attack_type(weapon) for weapon in weapons if weapon)
        else:
            range_type = (self.attack_type(),)
        return ', '.join(
            filter(
                None,
                (
                    self.get_action_type_display(),
                    self.get_accessory_type_display() if self.accessory_type else '',
                    self.get_frequency_display(),
                )
                + range_type
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

    @classmethod
    def parse_from_image(cls, img_file) -> dict:
        img = Image.open(img_file)
        text = image_to_string(img, lang='rus')
        # return Power.objects.create(**cls.parse_power_text(text))
        return cls.parse_power_text(text)

    @classmethod
    def parse_power_text(cls, text: str) -> dict:
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        result = {
            'name': '',
            'klass': None,
            'level': 0,
            'description': '',
            'frequency': '',
            'action_type': '',
            'accessory_type': '',
            'range_type': '',
            'range': 0,
            'burst': 0,
        }
        properties = {}
        current_line = 0
        try:
            if not lines:
                return result

            first_line = []
            for line in lines:
                first_line.append(line)
                current_line += 1
                if line.rstrip()[-1].isdigit():
                    break

            first_line = ' '.join(first_line)
            first_line_pattern = re.compile(r"^(.*?) (\S+) ([\w\-]+) (\d+)$")
            match = first_line_pattern.match(first_line)

            if match:
                name, _, class_genitive, level = match.groups()
                result['name'] = name.strip().capitalize()

                # Преобразование класса в именительный падеж
                match class_genitive:
                    case s if s.endswith("а"):
                        class_nominative = s.rstrip("а")
                    case s if s.endswith('ея'):
                        class_nominative = s.rstrip("я") + "й"
                    case s if s.endswith("я"):
                        class_nominative = s.rstrip("я") + "ь"
                    case _:
                        class_nominative = class_genitive
                class_nominative = class_nominative.capitalize()

                result['klass'] = Class.objects.get(name_display=class_nominative).pk

                try:
                    result['level'] = int(level)
                except ValueError:
                    pass

            description_lines = []
            while current_line < len(lines) and not any(
                lines[current_line].lower().startswith(keyword)
                for keyword in ["на сцену", "на день", "неограниченный"]
            ):
                description_lines.append(lines[current_line])
                current_line += 1
            result['description'] = (
                " ".join(description_lines) if description_lines else None
            )

            RANGE_PATTERNS = [
                (
                    re.compile(r'Рукопашное оружие', re.I),
                    {'range_type': 'Рукопашное оружие', 'range': 0, 'area': 0},
                ),
                (
                    re.compile(r'Рукопашное (\d+)', re.I),
                    {'range_type': 'Рукопашное', 'range': 1, 'area': 0},
                ),
                (
                    re.compile(r'Рукопашное касание', re.I),
                    {'range_type': 'Рукопашное касание', 'range': 0, 'area': 0},
                ),
                (
                    re.compile(r'Дальнобойное оружие', re.I),
                    {'range_type': 'Дальнобойное оружие', 'range': 0, 'area': 0},
                ),
                (
                    re.compile(r'Дальнобойный (\d+)', re.I),
                    {'range_type': 'Дальнобойный', 'range': 1, 'area': 0},
                ),
                (
                    re.compile(r'Дальнобойный видимость', re.I),
                    {'range_type': 'Дальнобойный видимость', 'range': 0, 'area': 0},
                ),
                (
                    re.compile(r'Ближняя вспышка (\d+)', re.I),
                    {'range_type': 'Вспышка', 'range': 0, 'area': 1},
                ),
                (
                    re.compile(r'Ближняя волна (\d+)', re.I),
                    {'range_type': 'Волна', 'range': 0, 'area': 1},
                ),
                (
                    re.compile(
                        r'Зональная вспышка (\d+) в пределах (\d+) клеток', re.I
                    ),
                    {'range_type': 'Вспышка', 'range': 2, 'area': 1},
                ),
                (
                    re.compile(r'Зональная стена (\d+) в пределах (\d+) клеток', re.I),
                    {'range_type': 'Стена', 'range': 2, 'area': 1},
                ),
                (
                    re.compile(r'Персональный', re.I),
                    {'range_type': 'Персональный', 'range': 0, 'area': 0},
                ),
            ]

            # === Обработка остальных параметров ===
            current_prop = None
            in_property = False

            for i in range(current_line, len(lines)):
                line = lines[i]

                # Обработка многострочных свойств
                prop_match = re.match(r'^([А-Яа-яЁё\s]+?):\s*(.*)', line)
                if prop_match:
                    raw_key = prop_match.group(1).strip().capitalize()
                    key = PowerPropertyTitle.get_by_description(
                        raw_key, default=PowerPropertyTitle.OTHER
                    ).value
                    value = prop_match.group(2).strip()
                    if key == PowerPropertyTitle.OTHER:
                        value = f'{raw_key}: {value}'
                    properties[key] = value
                    current_prop = key
                    in_property = True
                    continue
                elif in_property and current_prop:
                    properties[current_prop] += ' ' + line
                    continue

                # Поиск частоты использования
                if not result['frequency']:
                    freq_match = re.search(
                        r'(на\s*[сc]цену|на\s*день|неограниченный)', line, re.I
                    )
                    if freq_match:
                        result['frequency'] = PowerFrequencyIntEnum.get_by_description(
                            freq_match.group(0).capitalize()
                        )

                # Поиск типа действия
                if not result['action_type']:
                    for action in PowerActionTypeEnum:
                        if re.search(rf'^{re.escape(action.description)}', line, re.I):
                            result['action_type'] = action.value
                            break

                if not result['accessory_type']:
                    accessory_match = re.findall(r'(оружие|инструмент)', line, re.I)
                    if accessory_match:
                        result['accessory_type'] = list(
                            set(
                                [
                                    AccessoryTypeEnum.get_by_description(
                                        a.capitalize()
                                    ).value
                                    for a in accessory_match
                                ]
                            )
                        )

                if not result['range_type']:
                    for pattern, params in RANGE_PATTERNS:
                        match = pattern.search(line)
                        if match:
                            result['range_type'] = (
                                PowerRangeTypeEnum.get_by_description(
                                    params['range_type']
                                ).value
                            )

                            # Обработка числовых параметров
                            if 'range' in params:
                                if params['range'] != 0:
                                    result['range'] = int(match.group(params['range']))

                            if 'area' in params:
                                if params['area'] != 0:
                                    result['area'] = int(match.group(params['area']))
                            break

        except (ValueError, IndexError, AttributeError) as e:
            print(f"Ошибка парсинга: {str(e)}")

        ATTRIBUTE_ATTACK_MAP = {
            "Сила": "str",
            "Харизма": "cha",
            "Мудрость": "wis",
            "Ловкость": "dex",
            "Телосложение": "con",
            "Интеллект": "int",
        }

        ATTRIBUTE_MAP = {
            "Силы": "str",
            "Харизмы": "cha",
            "Мудрости": "wis",
            "Ловкости": "dex",
            "Телосложения": "con",
            "Интеллекта": "int",
        }

        i = 0
        for key, value in properties.items():
            if (
                key == PowerPropertyTitle.ATTACK
                or PowerPropertyTitle.ATTACK.lower() in value.split(':')[0].lower()
            ):
                match = re.match(
                    r"([а-яё]+)(?:\s*\+\s*(\d+))?\s+против\s+([а-яё]+)", value, re.I
                )
                if match:
                    attr, bonus, defense = match.groups()
                    attr_code = ATTRIBUTE_ATTACK_MAP.get(
                        attr.capitalize(), attr.lower()
                    )
                    new_value = f"${attr_code}+atk"

                    if bonus:
                        new_value += f"+{bonus}"

                    value = f"{new_value} против {defense}"
            else:
                # replace [Ор] to wpn+dmg
                value = re.sub(r'(\d+)\[Ор\.?\]', r'\1*wpn+dmg', value)

                # replace modifier titles to variables
                value = re.sub(
                    r'(?:ваш\s+)?модификатор\s+([а-яё]+)',
                    lambda m: ATTRIBUTE_MAP.get(
                        m.group(1).capitalize(), m.group(1).lower()
                    ),
                    value,
                    flags=re.I,
                )

                # remove spaces around +
                value = re.sub(r'\s*\+\s*', '+', value)

            result[f'properties-{i}-title'] = key
            result[f'properties-{i}-description'] = value
            result[f'properties-{i}-order'] = i
            i += 1
        return result


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
        verbose_name=_('Title'),
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
    """Mixin providing power calculation and expression evaluation capabilities.

    This mixin handles:
    - Expression parsing using Reverse Polish Notation for complex calculations
    - Dynamic power property evaluation based on character stats and equipment
    - Attack and damage bonus calculations
    - Weapon-specific power variations
    - Caching of calculated power displays for performance

    Used by NPC models to provide sophisticated power mechanics that adapt
    to character equipment, level, and abilities.
    """

    # Operator definitions for expression evaluation (function, precedence)
    OPERATORS = {
        '+': (operator.add, 0),  # Addition
        '-': (operator.sub, 0),  # Subtraction
        '*': (operator.mul, 1),  # Multiplication
        '/': (operator.floordiv, 1),  # Integer division
        '^': (max, 2),  # Maximum function
        '_': (min, 2),  # Minimum function
    }

    @property
    def _power_attrs(self: NPCProtocol) -> dict[PowerVariables | str, int]:
        """Dictionary mapping power variables to character attribute values."""
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
    ) -> bool:
        return (
            self._is_no_hand_implement_ki_focus
            and self.is_implement_proficient(self.no_hand)
            and accessory_type
            in (AccessoryTypeEnum.WEAPON, AccessoryTypeEnum.TWO_WEAPONS)
        )

    def _calculate_weapon_damage(
        self: NPCProtocol, weapon: 'Weapon', accessory_type: AccessoryTypeEnum | None
    ) -> DiceRoll:
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
    ) -> int:
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
        self: NPCProtocol, weapon: 'Weapon', accessory_type: AccessoryTypeEnum | None
    ) -> int:
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
        token: PowerVariables | str,
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
        """Evaluate expression in Reverse Polish Notation (RPN).

        Algorithm:
        1. Process tokens from left to right
        2. If token is a number/variable, parse it and push to stack
        3. If token is an operator, pop two values from stack and apply operation
        4. The final value in stack is the result

        Args:
            expression: RPN expression string (e.g., "str 3 + wpn +")
            accessory_type: Type of accessory being used
            weapon: Primary weapon for calculations
            secondary_weapon: Secondary weapon for calculations
            item: Magic item for calculations

        Returns:
            Calculated result as int or DiceRoll object
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
            id=power.pk,
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
