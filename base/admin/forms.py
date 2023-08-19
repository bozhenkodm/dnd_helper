from typing import Any

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError

from base.constants.constants import (
    DefenceTypeEnum,
    MagicItemSlot,
    NPCClassEnum,
    NPCCreationStepEnum,
    NPCRaceEnum,
    SexEnum,
    ShieldTypeIntEnum,
    SkillsEnum,
    WeaponHandednessEnum,
)
from base.models import NPC
from base.models.abilities import Ability
from base.models.magic_items import (
    ArmsSlotItem,
    FeetSlotItem,
    HandsSlotItem,
    HeadSlotItem,
    MagicItemType,
    NeckSlotItem,
    RingsSlotItem,
    SimpleMagicItem,
    WaistSlotItem,
)
from base.models.models import Armor, Weapon, WeaponType
from base.models.powers import Power
from base.models.skills import Skill
from base.objects import weapon_types_tuple
from base.objects.weapon_types import HolySymbol, KiFocus


class NPCModelForm(forms.ModelForm):
    class Meta:
        model = NPC
        fields = '__all__'

    sex = forms.ChoiceField(
        choices=SexEnum.generate_choices(is_sorted=False), label='Пол'
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.id:
            klass_data_instance = self.instance.klass_data_instance
            self.fields['var_bonus_ability'] = forms.ModelChoiceField(
                queryset=Ability.objects.filter(races=self.instance.race),
                label='Выборочный бонус характеристики',
                required=False,
            )
            self.fields['trained_skills'] = forms.ModelMultipleChoiceField(
                queryset=Skill.objects.filter(classes=self.instance.klass),
                widget=forms.CheckboxSelectMultiple,
                label='Тренированный навыки',
                required=False,
            )
            self.fields['powers'] = forms.ModelMultipleChoiceField(
                queryset=Power.objects.with_frequency_order()
                .filter(klass=self.instance.klass, level__lte=self.instance.level)
                .order_by('level', 'frequency_order'),
                label='Таланты',
                widget=FilteredSelectMultiple('Таланты', False),
                required=False,
            )
            if subclass_enum := getattr(klass_data_instance, 'SubclassEnum', None):
                self.fields['subclass'] = forms.TypedChoiceField(
                    coerce=int,
                    choices=subclass_enum.generate_choices(),
                    label='Подкласс',
                    required=self.instance.creation_step
                    == NPCCreationStepEnum.BASE_ABILITIES,
                )
            weapon_queryset = Weapon.objects.select_related(
                'weapon_type', 'magic_item_type'
            ).order_by('level', 'weapon_type__name', 'magic_item_type__name')
            if self.instance.weapons.count():
                weapon_queryset = weapon_queryset.filter(
                    id__in=self.instance.weapons.values_list('id', flat=True)
                )
            self.fields['primary_hand'] = forms.ModelChoiceField(
                queryset=weapon_queryset, label='Основная рука', required=False
            )
            self.fields['secondary_hand'] = forms.ModelChoiceField(
                queryset=weapon_queryset, label='Вторичная рука', required=False
            )
            self.fields['no_hand'] = forms.ModelChoiceField(
                queryset=Weapon.objects.select_related('weapon_type', 'magic_item_type')
                .filter(
                    weapon_type__slug__in=(KiFocus.slug(), HolySymbol.slug())
                    # TODO make it type, put it in database and filter by it
                )
                .order_by('level', 'weapon_type__name', 'magic_item_type__name'),
                label='Инструмент не в руку',
                required=False,
            )
            self.fields['neck_slot'] = forms.ModelChoiceField(
                queryset=NeckSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=NeckSlotItem.SLOT.value
                ),
                label='Предмет на шею',
                required=False,
            )
            self.fields['head_slot'] = forms.ModelChoiceField(
                queryset=HeadSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=HeadSlotItem.SLOT.value
                ),
                label='Предмет на голову',
                required=False,
            )
            self.fields['waist_slot'] = forms.ModelChoiceField(
                queryset=WaistSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=WaistSlotItem.SLOT.value
                ),
                label='Предмет на пояс',
                required=False,
            )
            self.fields['feet_slot'] = forms.ModelChoiceField(
                queryset=FeetSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=FeetSlotItem.SLOT.value
                ),
                label='Предмет на ноги',
                required=False,
            )
            self.fields['arms_slot'] = forms.ModelChoiceField(
                queryset=ArmsSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=ArmsSlotItem.SLOT.value
                ),
                label='Предмет на предплечья',
                required=False,
            )

            self.fields['left_ring_slot'] = forms.ModelChoiceField(
                queryset=RingsSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=RingsSlotItem.SLOT.value
                ),
                label='Кольцо на левую руку',
                required=False,
            )

            self.fields['right_ring_slot'] = forms.ModelChoiceField(
                queryset=RingsSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=RingsSlotItem.SLOT.value
                ),
                label='Кольцо на правую руку',
                required=False,
            )
            self.fields['gloves_slot'] = forms.ModelChoiceField(
                queryset=HandsSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=HandsSlotItem.SLOT.value
                ),
                label='Предмет на кисти',
                required=False,
            )

    def check_shield_and_weapon_in_one_hand(
        self, secondary_hand, shield_is_in_hand: bool
    ) -> None:
        if secondary_hand and shield_is_in_hand:
            error = ValidationError('Нельзя удержать в одной руке оружие и щит')
            self.add_error('arms_slot', error)
            self.add_error('secondary_hand', error)

    def check_two_handed_weapon_held_with_two_hands(
        self, primary_hand, secondary_hand, shield_is_in_hand: bool
    ) -> None:
        if (
            primary_hand
            and primary_hand.data_instance.handedness == WeaponHandednessEnum.TWO
        ):
            error = ValidationError(
                'Когда в основной руке двуручное оружие, вторая должна быть пустой'
            )
            if secondary_hand:
                self.add_error('secondary_hand', error)
            if shield_is_in_hand:
                self.add_error('arms_slot', error)

    def check_two_weapons_in_two_hands(self, primary_hand, secondary_hand) -> None:
        if (
            primary_hand
            and primary_hand.data_instance.handedness
            != WeaponHandednessEnum.TWO  # one-handed or versatile
            and secondary_hand
        ):
            klass_data_instance = self.instance.klass_data_instance
            if (
                (
                    klass_data_instance.slug == NPCClassEnum.RANGER
                    and self.cleaned_data['subclass']
                    == klass_data_instance.SubclassEnum.TWO_HANDED.value
                    or klass_data_instance.slug == NPCClassEnum.BARBARIAN
                    and self.cleaned_data['subclass']
                    == klass_data_instance.SubclassEnum.WHIRLING.value
                )
                and secondary_hand.data_instance.handedness == WeaponHandednessEnum.TWO
            ):
                self.add_error(
                    'secondary_hand',
                    ValidationError(
                        'Даже следопыты и варвары '
                        'не могут держать двуручное оружие во второй руке'
                    ),
                )
            elif not (
                klass_data_instance.slug == NPCClassEnum.RANGER
                and self.cleaned_data['subclass']
                == klass_data_instance.SubclassEnum.TWO_HANDED.value
                or klass_data_instance.slug == NPCClassEnum.BARBARIAN
                and self.cleaned_data['subclass']
                == klass_data_instance.SubclassEnum.WHIRLING.value
            ) and not (secondary_hand and secondary_hand.data_instance.is_off_hand):
                self.add_error(
                    'secondary_hand',
                    ValidationError(
                        'Во второй руке можно держать только дополнительное оружие'
                    ),
                )

    def check_proper_sex(self) -> None:
        if 'race' in self.cleaned_data:
            if (
                self.cleaned_data['race'].name == NPCRaceEnum.HAMADRYAD
                and self.cleaned_data['sex'] != SexEnum.F
            ):
                error = ValidationError('Гамадриады только женщины')
                self.add_error('sex', error)
                self.add_error('race', error)

            if (
                self.cleaned_data['race'].name == NPCRaceEnum.SATYR
                and self.cleaned_data['sex'] != SexEnum.M
            ):
                error = ValidationError('Сатиры только мужчины')
                self.add_error('sex', error)
                self.add_error('race', error)

    def check_pc_without_functional_template(self):
        if (
            not self.cleaned_data['is_bonus_applied']
            and self.cleaned_data['functional_template']
        ):
            message = (
                'Неигровые персонажи без бонуса уровня '
                'не могут иметь функциональный шаблон'
            )
            self.add_error('functional_template', message)
            self.add_error('is_bonus_applied', message)

    def check_npc_without_paragon_path(self):
        if (
            self.cleaned_data['is_bonus_applied']
            and self.cleaned_data['paragon_path']
        ):
            message = (
                'Неигровые персонажи c бонусом уровня '
                'не могут иметь путь совершенства'
            )
            self.add_error('paragon_path', message)
            self.add_error('is_bonus_applied', message)

    def clean(self) -> dict[str, Any] | None:
        self.instance: NPC
        if not self.instance.id:
            self.check_pc_without_functional_template()
            return super().clean()
        self.check_npc_without_paragon_path()
        primary_hand = self.cleaned_data.get('primary_hand')
        secondary_hand = self.cleaned_data.get('secondary_hand')
        shield_is_in_hand = bool(
            self.cleaned_data['arms_slot'] and self.cleaned_data['arms_slot'].shield
        )
        self.check_shield_and_weapon_in_one_hand(secondary_hand, shield_is_in_hand)
        self.check_two_handed_weapon_held_with_two_hands(
            primary_hand, secondary_hand, shield_is_in_hand
        )
        self.check_two_weapons_in_two_hands(primary_hand, secondary_hand)

        return super().clean()


class NPCModelForm__(forms.ModelForm):
    class Meta:
        model = NPC
        exclude = ('description', 'creation_step', 'creation_step')


class WeaponTypeForm(forms.ModelForm):
    class Meta:
        model = WeaponType
        fields = '__all__'

    slug = forms.ChoiceField(
        choices=[
            (cls.slug, f'{cls.name}')
            for cls in weapon_types_tuple
            if cls.slug not in set(WeaponType.objects.values_list('slug', flat=True))
        ],
        label='Название',
    )


class ItemAbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.magic_item_type:
            self.fields['level'] = forms.ChoiceField(
                choices=((i, i) for i in self.instance.magic_item_type.level_range()),
                label='Уровень',
            )


class WeaponForm(ItemAbstractForm):
    class Meta:
        model = Weapon
        fields = '__all__'


class ArmorForm(ItemAbstractForm):
    class Meta:
        model = Armor
        fields = '__all__'


class MagicItemForm(ItemAbstractForm):
    class Meta:
        model = SimpleMagicItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MagicItemForm, self).__init__(*args, **kwargs)
        self.fields['magic_item_type'].required = True


class ArmsSlotItemForm(ItemAbstractForm):
    class Meta:
        model = ArmsSlotItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArmsSlotItemForm, self).__init__(*args, **kwargs)
        self.fields['magic_item_type'].queryset = MagicItemType.objects.filter(
            slots__contains=MagicItemSlot.ARMS.value
        )

    shield = forms.ChoiceField(
        choices=ShieldTypeIntEnum.generate_choices(),
        label='Щит',
        initial=ShieldTypeIntEnum.NONE,
    )


class MagicItemTypeForm(forms.ModelForm):
    class Meta:
        model = MagicItemType
        fields = '__all__'

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена', initial=False
    )

    acrobatics = forms.CharField(required=False, label='Акробатика')
    arcana = forms.CharField(required=False, label='Магия')
    athletics = forms.CharField(required=False, label='Атлетика')
    bluff = forms.CharField(required=False, label='Обман')
    diplomacy = forms.CharField(required=False, label='Переговоры')
    dungeoneering = forms.CharField(required=False, label='Подземелья')
    endurance = forms.CharField(required=False, label='Выносливость')
    heal = forms.CharField(required=False, label='Целительство')
    history = forms.CharField(required=False, label='История')
    insight = forms.CharField(required=False, label='Проницательность')
    intimidate = forms.CharField(required=False, label='Запугивание')
    nature = forms.CharField(required=False, label='Природа')
    perception = forms.CharField(required=False, label='Внимательность')
    religion = forms.CharField(required=False, label='Религия')
    stealth = forms.CharField(required=False, label='Скрытность')
    streetwise = forms.CharField(required=False, label='Знание улиц')
    thievery = forms.CharField(required=False, label='Воровство')

    armor_class = forms.CharField(required=False, label='КД')
    fortitude = forms.CharField(required=False, label='Стойкость')
    reflex = forms.CharField(required=False, label='Реакция')
    will = forms.CharField(required=False, label='Воля')

    resist_acid = forms.CharField(required=False, label='Кислота')
    resist_cold = forms.CharField(required=False, label='Холод')
    resist_fire = forms.CharField(required=False, label='Огонь')
    resist_lightning = forms.CharField(required=False, label='Электричество')
    resist_necrotic = forms.CharField(required=False, label='Некротическая энергия')
    resist_poison = forms.CharField(required=False, label='Яд')
    resist_psychic = forms.CharField(required=False, label='Психическая энергия')
    resist_radiant = forms.CharField(required=False, label='Излучение')
    resist_thunder = forms.CharField(required=False, label='Звук')
    resist_force = forms.CharField(required=False, label='Силовое поле')

    # Bonuses to saving throws
    save_charm = forms.CharField(required=False, label='Очарование')
    save_conjuration = forms.CharField(required=False, label='Иллюзия')
    save_fear = forms.CharField(required=False, label='Страх')
    save_sleep = forms.CharField(required=False, label='Сон')
    save_acid = forms.CharField(required=False, label='Кислота')
    save_cols = forms.CharField(required=False, label='Холод')
    save_fire = forms.CharField(required=False, label='Огонь')
    save_lightning = forms.CharField(required=False, label='Электричество')
    save_necrotic = forms.CharField(required=False, label='Некротическая энергия')
    save_poison = forms.CharField(required=False, label='Яд')
    save_slow = forms.CharField(required=False, label='Замедление')
    save_immobilized = forms.CharField(required=False, label='Обездвиживание')
    save_restrained = forms.CharField(required=False, label='Удерживание')
    save_damage = forms.CharField(required=False, label='Урон')
    # TODO add the rest of conditions that can be saved

    speed = forms.CharField(required=False, label='Скорость')
    initiative = forms.CharField(required=False, label='Инициатива')
    melee_damage = forms.CharField(required=False, label='Рукопашный урон')
    range_damage = forms.CharField(required=False, label='Дальнобойный урон')

    def __init__(self, *args, **kwargs):
        super(MagicItemTypeForm, self).__init__(*args, **kwargs)
        properties = self.instance.properties
        properties = properties or {
            'defences': {},
            'skills': {},
            'resist': {},
            'save': {},
        }
        for defence in DefenceTypeEnum:
            self.initial[defence] = properties['defences'].get(defence, '')

    def clean(self):
        super(MagicItemTypeForm, self).clean()
        properties = {
            'defences': {},
            'skills': {},
            'resist': {},
            'save': {},
        }
        skills = {}
        for skill in SkillsEnum:
            field = skill.value.lower()
            if self.cleaned_data[field]:
                skills[field] = self.cleaned_data[field]
        if skills:
            properties['skills'] = skills
        defences = {}
        for defence in DefenceTypeEnum:
            field = defence.value.lower()
            if self.cleaned_data[field]:
                defences[field] = self.cleaned_data[field]
        if defences:
            properties['defences'] = defences
        self.cleaned_data['properties'] = properties
