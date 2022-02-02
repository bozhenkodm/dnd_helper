from dataclasses import asdict

from django import forms
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectFormField  # type: ignore

from base.constants.constants import (
    AbilitiesEnum,
    NPCClassEnum,
    NPCRaceEnum,
    SexEnum,
    SkillsEnum,
    WeaponHandednessEnum,
)
from base.models import NPC
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
from base.objects import weapon_types_tuple


class NPCModelForm(forms.ModelForm):
    class Meta:
        model = NPC
        fields = '__all__'

    sex = forms.ChoiceField(
        choices=SexEnum.generate_choices(is_sorted=False), label='Пол'
    )

    def __init__(self, *args, **kwargs):
        super(NPCModelForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['var_bonus_ability'] = forms.ChoiceField(
                choices=[
                    (key.upper(), AbilitiesEnum[key.upper()].description)
                    for key, value in asdict(
                        self.instance.race_data_instance.var_ability_bonus
                    ).items()
                    if value
                ],
                label='Выборочный бонус характеристики',
                required=False,
            )
            choices = self.instance.klass_data_instance.trainable_skills
            self.fields['trained_skills'] = MultiSelectFormField(
                choices=(
                    (key.upper(), SkillsEnum[key.upper()].description)
                    for key, value in asdict(choices).items()
                    if value
                ),
                widget=forms.CheckboxSelectMultiple,
                label='Тренированный навыки',
            )
            self.fields['powers'] = forms.ModelMultipleChoiceField(
                queryset=Power.objects.with_frequency_order()
                .filter(klass=self.instance.klass, level__lte=self.instance.level)
                .order_by('level', 'frequency_order'),
                label='Таланты',
            )
            if subclass_enum := getattr(
                self.instance.klass_data_instance, 'SubclassEnum', None
            ):
                self.fields['subclass'] = forms.TypedChoiceField(
                    coerce=int,
                    choices=subclass_enum.generate_choices(),
                    label='Подкласс',
                )
            weapon_queryset = Weapon.objects.all()
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
            self.fields['hands_slot'] = forms.ModelChoiceField(
                queryset=HandsSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slots__contains=HandsSlotItem.SLOT.value
                ),
                label='Предмет на кисти',
                required=False,
            )

    def clean(self):
        self.instance: NPC
        if not self.instance.id:
            return super(NPCModelForm, self).clean()
        primary_hand = self.cleaned_data.get('primary_hand')
        secondary_hand = self.cleaned_data.get('secondary_hand')
        if secondary_hand and self.cleaned_data['shield']:
            error = ValidationError('Нельзя удержать в одной руке оружие и щит')
            self.add_error('shield', error)
            self.add_error('secondary_hand', error)
        if (
            primary_hand
            and primary_hand.data_instance.handedness == WeaponHandednessEnum.TWO
        ):
            error = ValidationError(
                'Когда в основной руке двуручное оружие, вторая должна быть пустой'
            )
            if secondary_hand:
                self.add_error('secondary_hand', error)
            if self.cleaned_data['shield']:
                self.add_error('shield', error)
        if (
            primary_hand
            and primary_hand.data_instance.handedness
            != WeaponHandednessEnum.TWO  # one-handed or versatile
            and secondary_hand
        ):
            klass_data_instance = self.instance.klass_data_instance
            if (
                (
                    klass_data_instance.slug == NPCClassEnum.RANGER_MELEE
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
                klass_data_instance.slug == NPCClassEnum.RANGER_MELEE
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

        super(NPCModelForm, self).clean()


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
                choices=(
                    (i, i)
                    for i in range(
                        self.instance.magic_item_type.min_level,
                        31,
                        self.instance.magic_item_type.step,
                    )
                ),
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


class MagicItemTypeForm(forms.ModelForm):
    class Meta:
        model = MagicItemType
        fields = '__all__'

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена', initial=False
    )
