import re
from functools import cached_property
from typing import Optional, Sequence

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from multiselectfield import MultiSelectField  # type: ignore

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import (
    AbilitiesEnum,
    AccessoryTypeEnum,
    ArmorTypeIntEnum,
    DefenceTypeEnum,
    DiceIntEnum,
    MagicItemCategory,
    NPCClassEnum,
    NPCRaceEnum,
    PowerActionTypeEnum,
    PowerDamageTypeEnum,
    PowerEffectTypeEnum,
    PowerFrequencyEnum,
    PowerPropertyTitle,
    PowerRangeTypeEnum,
    PowersVariables,
    SexEnum,
    ShieldTypeEnum,
    SkillsEnum,
)
from base.managers import PowerQueryset, WeaponTypeQuerySet
from base.models.mixins.abilities import AttributeAbstract
from base.models.mixins.defences import DefenceMixin
from base.models.mixins.skills import SkillMixin
from base.objects import npc_klasses, race_classes, weapon_types_classes
from base.objects.dice import DiceRoll
from base.objects.powers_output import PowerDisplay, PowerPropertyDisplay


class MagicItem(models.Model):
    class Meta:
        verbose_name = 'Магический предмет'
        verbose_name_plural = 'Магические предметы'

    name = models.CharField(verbose_name='Название', max_length=100)
    min_level = models.PositiveSmallIntegerField(
        verbose_name='Минимальный уровень', default=1
    )
    step = models.PositiveSmallIntegerField('Шаг повышения уровня', default=5)
    category = models.CharField(
        verbose_name='Категория',
        choices=MagicItemCategory.generate_choices(is_sorted=False),
        default=MagicItemCategory.UNCOMMON,
        max_length=MagicItemCategory.max_length(),
    )
    picture = models.ImageField(
        verbose_name='Картинка', null=True, upload_to='items', blank=True
    )
    source = models.CharField(
        verbose_name='Источник',
        max_length=20,
        help_text='Книга и страница',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class ItemAbstract(models.Model):
    class Meta:
        abstract = True

    magic_item = models.ForeignKey(
        MagicItem,
        verbose_name='Магический предмет',
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    level = models.SmallIntegerField(verbose_name='Уровень', default=0)

    @property
    def enchantment(self):
        if not self.magic_item:
            return 0
        return (self.level - 1) // 5 + 1

    @property
    def price(self):
        if not self.level:
            return 0
        return (200 + (self.level % 5) * 160) * (5 ** (self.level // 5))


class Armor(ItemAbstract):
    class Meta:
        verbose_name = 'Доспех'
        verbose_name_plural = 'Доспехи'

    armor_type = models.SmallIntegerField(
        verbose_name='Тип',
        choices=ArmorTypeIntEnum.generate_choices(),
    )
    bonus_armor_class = models.SmallIntegerField(
        verbose_name='Дополнительный класс доспеха',
        default=0,
        help_text='Для магических доспехов высоких уровней',
    )
    speed_penalty = models.SmallIntegerField(verbose_name='Штраф скорости', default=0)
    skill_penalty = models.SmallIntegerField(verbose_name='Штраф навыков', default=0)

    def __str__(self):
        return f'{self.name}, +{self.enchantment}'

    @property
    def armor_class(self):
        return self.armor_type + self.bonus_armor_class

    @property
    def name(self):
        if not self.magic_item:
            return self.get_armor_type_display()
        return f'{self.get_armor_type_display()}, {self.magic_item.name}'

    @property
    def is_light(self):
        return self.armor_type in (
            ArmorTypeIntEnum.CLOTH,
            ArmorTypeIntEnum.LEATHER,
            ArmorTypeIntEnum.HIDE,
        )


class WeaponType(models.Model):
    class Meta:
        verbose_name = 'Тип оружия'
        verbose_name_plural = 'Типы оружия'

    objects = WeaponTypeQuerySet.as_manager()

    name = models.CharField(verbose_name='Название', max_length=30)
    slug = models.CharField(verbose_name='Slug', max_length=30, unique=True)

    def __str__(self):
        return self.name

    @cached_property
    def data_instance(self):
        return weapon_types_classes.get(self.slug)()

    def damage(self, weapon_number=1):
        return (
            f'{self.data_instance.dice_number*weapon_number}'
            f'{self.data_instance.damage_dice.description}'
        )


class Weapon(ItemAbstract):
    class Meta:
        verbose_name = 'Оружие'
        verbose_name_plural = 'Оружие'
        unique_together = ('magic_item', 'level', 'weapon_type')

    weapon_type = models.ForeignKey(
        WeaponType, verbose_name='Тип оружия', on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return f'{self.title}, +{self.enchantment}'

    @property
    def title(self) -> str:
        if not self.magic_item:
            return str(self.weapon_type)
        return f'{self.weapon_type}, {self.magic_item}'

    @property
    def damage(self):
        if not self.enchantment:
            return (
                f'{self.data_instance.dice_number}'
                f'{self.data_instance.damage_dice.description}'
            )
        return (
            f'{self.data_instance.dice_number}'
            f'{self.data_instance.damage_dice.description} + '
            f'{self.enchantment}'
        )

    @property
    def damage_roll(self):
        return DiceRoll(
            rolls=self.weapon_type.data_instance.dice_number,
            dice=self.weapon_type.data_instance.damage_dice,
            addendant=self.enchantment,
        )

    @property
    def data_instance(self):
        return self.weapon_type.data_instance

    @property
    def prof_bonus(self):
        return self.data_instance.prof_bonus

    def get_attack_type(self, is_melee: bool, is_ranged: bool):
        melee_attack_type, ranged_attack_type = '', ''
        if is_melee:
            distance = 2 if self.data_instance.is_reach else 1
            melee_attack_type = f'Рукопашный {distance}'
        if is_ranged:
            ranged_attack_type = (
                f'Дальнобойный '
                f'{self.data_instance.range}/{self.data_instance.max_range}'
            )
        return (
            (is_melee and is_ranged and f'{melee_attack_type} или {ranged_attack_type}')
            or (is_melee and melee_attack_type)
            or (is_ranged and ranged_attack_type)
        )


class Race(models.Model):
    class Meta:
        verbose_name = 'Раса'
        verbose_name_plural = 'Расы'

    name = models.CharField(
        verbose_name='Название',
        max_length=NPCRaceEnum.max_length(),
        choices=NPCRaceEnum.generate_choices(),
        unique=True,
    )
    is_sociable = models.BooleanField(
        verbose_name='Социальная раса',
        default=True,
        help_text='Социальные расы используются для случайной генерации NPC',
    )

    def __str__(self):
        return NPCRaceEnum[self.name].description


class Class(models.Model):
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ('name_display',)

    name = models.SlugField(
        choices=NPCClassEnum.generate_choices(is_sorted=False),
        max_length=NPCClassEnum.max_length(),
    )
    name_display = models.CharField(
        verbose_name='Название',
        max_length=NPCClassEnum.max_description_length(),
    )

    def __str__(self):
        return self.name_display


class FunctionalTemplate(models.Model):
    class Meta:
        verbose_name = 'Функциональный шаблон'
        verbose_name_plural = 'Функциональные шаблоны'
        ordering = ('title',)

    title = models.CharField(max_length=50, null=False, verbose_name='Название')
    min_level = models.SmallIntegerField(verbose_name='Минимальный уровень', default=0)
    armor_class_bonus = models.SmallIntegerField(verbose_name='Бонус КД', default=0)
    fortitude_bonus = models.SmallIntegerField(
        verbose_name='Бонус стойкости', default=0
    )
    reflex_bonus = models.SmallIntegerField(verbose_name='Бонус реакции', default=0)
    will_bonus = models.SmallIntegerField(verbose_name='Бонус воли', default=0)
    save_bonus = models.SmallIntegerField(verbose_name='Бонус спасбросков', default=2)
    action_points_bonus = models.SmallIntegerField(
        verbose_name='Дополнительные очки действия', default=1
    )
    hit_points_per_level = models.SmallIntegerField(
        verbose_name='Хиты за уровень', default=8
    )

    def __str__(self):
        return self.title


class Power(models.Model):
    class Meta:
        verbose_name = 'Талант'
        verbose_name_plural = 'Таланты'
        # base_manager_name = 'PowerManager'

    objects = PowerQueryset.as_manager()

    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    frequency = models.CharField(
        verbose_name='Частота использования',
        choices=PowerFrequencyEnum.generate_choices(is_sorted=False),
        max_length=PowerFrequencyEnum.max_length(),
    )
    action_type = models.CharField(
        verbose_name='Действие',
        choices=PowerActionTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerActionTypeEnum.max_length(),
        default=PowerActionTypeEnum.STANDARD,
        null=True,
        blank=False,
    )
    klass = models.ForeignKey(
        Class,
        related_name='powers',
        verbose_name='Класс',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    subclass = models.SmallIntegerField(
        verbose_name='Подкласс',
        default=0,
    )
    race = models.ForeignKey(
        Race,
        verbose_name='Раса',
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name='powers',
    )
    functional_template = models.ForeignKey(
        FunctionalTemplate,
        verbose_name='Функциональный шаблон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='powers',
    )
    magic_item = models.ForeignKey(
        MagicItem,
        verbose_name='Магический предмет',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='powers',
    )
    level = models.SmallIntegerField(verbose_name='Уровень', default=0)
    attack_ability = models.CharField(
        verbose_name='Атакующая характеристика',
        choices=AbilitiesEnum.generate_choices(is_sorted=False),
        max_length=AbilitiesEnum.max_length(),
        null=True,
        blank=True,
    )
    attack_bonus = models.SmallIntegerField(verbose_name='Бонус атаки', default=0)
    defence = models.CharField(
        verbose_name='Против защиты',
        choices=DefenceTypeEnum.generate_choices(is_sorted=False),
        max_length=DefenceTypeEnum.max_length(),
        null=True,
        blank=True,
    )
    effect_type = MultiSelectField(
        verbose_name='Тип эффекта',
        choices=PowerEffectTypeEnum.generate_choices(),
        default=PowerEffectTypeEnum.NONE,
    )
    damage_type = MultiSelectField(
        verbose_name='Тип урона',
        choices=PowerDamageTypeEnum.generate_choices(),
        default=PowerDamageTypeEnum.NONE,
    )
    dice_number = models.SmallIntegerField(verbose_name='Количество кубов', default=1)
    damage_dice = models.SmallIntegerField(
        verbose_name='Кость урона',
        choices=DiceIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    accessory_type = models.CharField(
        verbose_name='Тип вооружения',
        choices=AccessoryTypeEnum.generate_choices(),
        max_length=AccessoryTypeEnum.max_length(),
        null=True,
        blank=True,
    )
    available_weapon_types = models.ManyToManyField(
        WeaponType,
        verbose_name='Требования к оружию',
        help_text='для талантов с оружием',
        blank=True,
    )
    range_type = models.CharField(
        verbose_name='Дальность',
        choices=PowerRangeTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerRangeTypeEnum.max_length(),
        default=PowerRangeTypeEnum.PERSONAL,
    )
    range = models.SmallIntegerField(verbose_name='Дальность', default=0)
    burst = models.SmallIntegerField(verbose_name='Площадь', default=0)

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
        if self.magic_item:
            return f'{self.name} - {self.magic_item}'
        return self.name

    @property
    def defence_subjanctive(self):
        if self.defence == DefenceTypeEnum.ARMOR_CLASS:
            return self.get_defence_display()
        return self.get_defence_display()[:-1] + 'и'

    @property
    def damage(self):
        return f'{self.dice_number}{self.get_damage_dice_display()}'

    def category(self, primary_weapon: Weapon = None, secondary_weapon: Weapon = None):
        if self.magic_item:
            return self.magic_item.name
        if self.functional_template:
            return self.functional_template.title
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
        raise ValueError('Power unproperly configured')

    def attack_type(self, weapon: Optional[Weapon] = None):
        if (
            self.range_type
            in (
                PowerRangeTypeEnum.MELEE_RANGED_WEAPON,
                PowerRangeTypeEnum.MELEE_WEAPON,
                PowerRangeTypeEnum.RANGED_WEAPON,
            )
            and weapon
        ):
            # TODO maybe move it to npc model
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
        raise ValueError('Wrong attack type')

    def keywords(self, weapon: Optional[Weapon] = None):
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


class PowerProperty(models.Model):
    power = models.ForeignKey(
        Power,
        verbose_name='Талант',
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
    level = models.SmallIntegerField(verbose_name='Уровень', default=1)
    subclass = models.SmallIntegerField(
        verbose_name='Подкласс',
        choices=IntDescriptionSubclassEnum.generate_choices(),
        default=0,
    )
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    order = models.SmallIntegerField(verbose_name='Порядок', default=0)

    def get_displayed_title(self):
        if self.title and self.title != PowerPropertyTitle.OTHER:
            return self.get_title_display()
        return self.description.split(':')[0]

    def get_displayed_description(self):
        if self.title and self.title != PowerPropertyTitle.OTHER:
            return self.description
        return '.'.join(self.description.split(':')[1:])

    def __str__(self):
        return f'{self.title} {self.description} {self.level}'


class NPC(DefenceMixin, AttributeAbstract, SkillMixin, models.Model):
    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCS'

    name = models.CharField(verbose_name='Имя', max_length=50)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        verbose_name='Раса',
    )
    klass = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name='Класс',
    )
    subclass = models.SmallIntegerField(
        verbose_name='Подкласс',
        default=0,
    )
    functional_template = models.ForeignKey(
        FunctionalTemplate,
        on_delete=models.CASCADE,
        verbose_name='Функциональный шаблон',
        null=True,
        blank=True,
    )
    sex = models.CharField(
        max_length=SexEnum.max_length(),
        choices=SexEnum.generate_choices(is_sorted=False),
        verbose_name='Пол',
    )
    level = models.PositiveSmallIntegerField(
        verbose_name='Уровень',
    )

    trained_skills = MultiSelectField(
        verbose_name='Тренированные навыки',
        choices=SkillsEnum.generate_choices(),
        min_choices=1,
        null=True,
        blank=True,
    )

    armor = models.ForeignKey(
        Armor, verbose_name='Доспехи', null=True, on_delete=models.SET_NULL
    )
    shield = models.CharField(
        verbose_name='Щит',
        max_length=5,
        choices=ShieldTypeEnum.generate_choices(),
        null=True,
        blank=True,
    )
    weapons = models.ManyToManyField(
        Weapon,
        verbose_name='Вооружение',
        blank=True,
        help_text=(
            'Имеющееся у персонажа вооружение. '
            'Если список не пустой, то оружие в руки выбирается из него.'
        ),
    )
    primary_hand = models.ForeignKey(
        Weapon,
        verbose_name='Основная рука',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_primary_hands',
    )
    secondary_hand = models.ForeignKey(
        Weapon,
        verbose_name='Вторичная рука',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_secondary_hands',
    )

    powers = models.ManyToManyField(Power, blank=True)

    def __str__(self):
        return (
            f'{self.name}'
            f'{f" ({self.functional_template}) " if self.functional_template else " "}'
            f'{self.race} {self.klass} {self.level} уровня'
        )

    # TODO these two next methods are shitshow,
    #  appeared to be parallel structures of race and class
    #  instead of complementing models.
    #  how to integrate npc instance to these instances and initialise them
    #  in race and class models respectively?

    @cached_property
    def race_data_instance(self):
        return race_classes.get(self.race.name)(npc=self)

    @cached_property
    def klass_data_instance(self):
        return npc_klasses.get(self.klass.name)(npc=self)

    @property
    def url(self):
        return reverse('npc', kwargs={'pk': self.pk})

    @property
    def half_level(self):
        return self.level // 2

    @property
    def _magic_threshold(self) -> int:
        """ Магический порог (максимальный бонус от магических предметов)"""
        return (self.level - 1) // 5

    @property
    def _level_bonus(self) -> int:
        """ Условный бонус к защитам, атакам и урону для мастерских персонажей"""
        return self._magic_threshold * 2 + 1

    @property
    def max_hit_points(self) -> int:
        result = (
            self.klass_data_instance.hit_points_per_level * self.level
            + self.constitution
            + self.klass_data_instance.hit_points_bonus
        )
        if self.functional_template:
            result += (
                self.functional_template.hit_points_per_level * self.level
                + self.constitution
            )
        return result

    @property
    def bloodied(self) -> int:
        return self.max_hit_points // 2

    @property
    def surge(self) -> int:
        """
        Исцеление
        """
        return self.bloodied // 2 + self.race_data_instance.healing_surge_bonus

    @property
    def _tier(self):
        """Этап развития"""
        if self.level < 11:
            return 0
        if self.level >= 21:
            return 2
        return 1

    @property
    def surges(self) -> int:
        """Количество исцелений"""
        return self._tier + 1 + self.race_data_instance.surges_number_bonus

    @property
    def initiative(self) -> int:
        return self.dex_mod + self.half_level + self.race_data_instance.initiative

    @property
    def speed(self):
        if self.armor:
            return self.race_data_instance.speed - min(
                self.armor.speed_penalty,
                self.race_data_instance.heavy_armor_speed_penalty,
            )
        return self.race_data_instance.speed

    @property
    def weapons_in_hands(self) -> Sequence[Weapon]:
        return tuple(filter(None, (self.primary_hand, self.secondary_hand)))

    @property
    def magic_items(self) -> Sequence[ItemAbstract]:
        return tuple(
            filter(
                lambda x: x and getattr(x, 'magic_item', False),
                # TODO add the rest of magic items
                (self.primary_hand, self.secondary_hand, self.armor),  # type: ignore
            )
        )

    def is_weapon_proficient(self, weapon) -> bool:
        data_instance = weapon.weapon_type.data_instance
        return any(
            (
                data_instance.category
                in map(int, self.klass_data_instance.available_weapon_categories),
                type(data_instance) in self.klass_data_instance.available_weapon_types,
                type(data_instance) in self.race_data_instance.available_weapon_types,
            )
        )

    def is_implement_proficient(self, weapon) -> bool:
        return (
            type(weapon.data_instance)
            in self.klass_data_instance.available_implement_types
        )

    def is_weapon_proper_for_power(
        self, power: Power, weapon: Optional[Weapon] = None
    ) -> bool:
        weapon = weapon or self.primary_hand or self.secondary_hand
        if not weapon:
            return False
        available_weapon_types = power.available_weapon_types
        if (
            available_weapon_types.count()
            and weapon.weapon_type not in available_weapon_types.all()
        ):
            return False
        if power.accessory_type == AccessoryTypeEnum.IMPLEMENT:
            return self.is_implement_proficient(weapon)
        if (
            power.accessory_type == AccessoryTypeEnum.WEAPON
            and power.accessory_type
            in (AccessoryTypeEnum.WEAPON, AccessoryTypeEnum.TWO_WEAPONS)
        ):
            # pure implements can't be used with weapon powers
            return not weapon.weapon_type.data_instance.is_pure_implement
        return False

    @property
    def inventory_text(self):
        return list(
            filter(
                None,
                list(
                    str(weapon)
                    for weapon in (self.weapons.all() or self.weapons_in_hands)
                )
                + [str(self.armor)]
                + [self.get_shield_display()],
            )
        )

    @property
    def power_attrs(self):
        return {
            PowersVariables.STR: self.str_mod,
            PowersVariables.CON: self.con_mod,
            PowersVariables.DEX: self.dex_mod,
            PowersVariables.INT: self.int_mod,
            PowersVariables.WIS: self.wis_mod,
            PowersVariables.CHA: self.cha_mod,
            PowersVariables.LVL: self.level,
        }

    def parse_string(
        self,
        power: Power,
        string: str,
        weapon: Weapon = None,
        secondary_weapon: Weapon = None,
        item: Optional[ItemAbstract] = None,
    ):  # TODO something with function signature
        pattern = r'\$([^\s]{3,})\b'  # gets substing from '$' to next whitespace
        expressions = re.findall(pattern, string)
        template = re.sub(
            pattern, '{}', string
        )  # preparing template for format() method
        calculated_expressions = []
        # calculating without operations order for now, just op for op
        # TODO fix with polish record
        # TODO rename variables!
        for expression in expressions:
            parsed_expression = re.findall(r'[a-z]{3}|[+\-*/]|[0-9]{0,2}', expression)
            current_calculated_expression = 0
            current_operation = None
            for parsed_expression_element in parsed_expression[:-1]:
                # iterating trough parsed_expression[:-1] because last element is ''
                if parsed_expression_element in ('+', '-', '*', '/'):
                    current_operation = parsed_expression_element
                    continue
                if parsed_expression_element == PowersVariables.WPN:
                    weapon = weapon or self.primary_hand
                    if not weapon:
                        raise ValueError('У данного таланта нет оружия')
                    current_element = weapon.damage_roll.treshhold(
                        self._magic_threshold
                    )
                elif parsed_expression_element == PowersVariables.WPS:
                    if not secondary_weapon:
                        raise ValueError('У данного таланта нет дополнительного оружия')
                    current_element = secondary_weapon.damage_roll.treshhold(
                        self._magic_threshold
                    )
                elif parsed_expression_element == PowersVariables.ATK:
                    current_element = (
                        self.klass_data_instance.attack_bonus(
                            weapon,
                            is_implement=power.accessory_type
                            == AccessoryTypeEnum.IMPLEMENT,
                        )
                        # armament enchantment
                        + max(
                            weapon and weapon.enchantment or 0 - self._magic_threshold,
                            0,
                        )
                        # power attack bonus should be added
                        # to string when creating power property
                    )
                elif parsed_expression_element == PowersVariables.DMG:
                    # TODO separate damage bonus and enchantment
                    current_element = self.klass_data_instance.damage_bonus + max(
                        weapon and weapon.enchantment or 0 - self._magic_threshold, 0
                    )
                elif parsed_expression_element == PowersVariables.EHT:
                    current_element = max(
                        weapon and weapon.enchantment or 0 - self._magic_threshold, 0
                    )
                elif parsed_expression_element == PowersVariables.ITL:
                    if not item:
                        raise ValueError('У данного таланта нет магического предмета')
                    current_element = item.level
                elif parsed_expression_element.isdigit():
                    current_element = int(parsed_expression_element)
                else:
                    current_element = self.power_attrs.get(parsed_expression_element)
                if current_operation == '+':
                    current_calculated_expression += current_element
                elif current_operation == '-':
                    current_calculated_expression -= current_element
                elif current_operation == '*':
                    current_calculated_expression = (
                        current_calculated_expression * current_element
                    )
                elif current_operation == '/':
                    current_calculated_expression //= current_element
                else:
                    current_calculated_expression = current_element
            calculated_expressions.append(current_calculated_expression)
        result = template.format(*calculated_expressions)
        # TODO remove injection weakness, leaving only markdown tags
        return mark_safe('<br>'.join(result.split('\n')))

    def valid_properties(self, power: Power):
        # TODO add comments, what's going on
        properties: dict[str, PowerProperty] = {}
        for prop in power.properties.filter(
            level__lte=self.level, subclass__in=(self.subclass, 0)
        ).order_by('-subclass'):
            key = f'{prop.get_displayed_title()},{prop.order}'
            if key not in properties or properties[key].level < prop.level:
                properties[key] = prop
        return sorted(properties.values(), key=lambda x: x and x.order)

    def powers_calculated(self):
        powers_qs = self.race.powers.filter(level=0)
        powers_qs |= self.powers.filter(
            models.Q(accessory_type__isnull=True) | models.Q(accessory_type='')
        )
        if self.functional_template:
            powers_qs |= self.functional_template.powers.filter(level=0)

        powers = []
        for power in powers_qs.ordered_by_frequency():
            powers.append(
                PowerDisplay(
                    name=power.name,
                    keywords=power.keywords(),
                    category=power.category(),
                    description=self.parse_string(power, string=power.description),
                    frequency_order=power.frequency_order,
                    properties=[
                        PowerPropertyDisplay(
                            title=prop.get_displayed_title(),
                            description=self.parse_string(
                                power, string=prop.get_displayed_description()
                            ),
                            debug=prop.get_displayed_description(),
                        )
                        for prop in self.valid_properties(power)
                    ],
                ).asdict()
            )
        for power in self.powers.ordered_by_frequency().filter(
            accessory_type__in=(AccessoryTypeEnum.WEAPON, AccessoryTypeEnum.IMPLEMENT)
        ):
            for weapon in self.weapons_in_hands:
                if not self.is_weapon_proper_for_power(power=power, weapon=weapon):
                    continue
                powers.append(
                    PowerDisplay(
                        name=power.name,
                        keywords=power.keywords(weapon),
                        category=power.category(weapon),
                        description=self.parse_string(power, power.description),
                        frequency_order=power.frequency_order,
                        properties=[
                            PowerPropertyDisplay(
                                **{
                                    'title': prop.get_displayed_title(),
                                    'description': self.parse_string(
                                        power,
                                        string=prop.get_displayed_description(),
                                        weapon=weapon,
                                    ),
                                    'debug': prop.description,
                                }
                            )
                            for prop in self.valid_properties(power)
                        ],
                    ).asdict()
                )
        for item in self.magic_items:
            for power in item.magic_item.powers.ordered_by_frequency():
                powers.append(
                    PowerDisplay(
                        name=power.name,
                        keywords=power.keywords(),
                        category=power.category(),
                        description=self.parse_string(power, power.description),
                        frequency_order=power.frequency_order,
                        properties=[
                            PowerPropertyDisplay(
                                **{
                                    'title': prop.get_displayed_title(),
                                    'description': self.parse_string(
                                        power,
                                        string=prop.get_displayed_description(),
                                        item=item,
                                    ),
                                    'debug': prop.description,
                                }
                            )
                            for prop in self.valid_properties(power)
                        ],
                    ).asdict()
                )

        return sorted(powers, key=lambda x: x['frequency_order'])
