from typing import Any

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError

from base.constants.constants import (
    MagicItemSlot,
    NPCClassEnum,
    NPCRaceEnum,
    SexEnum,
    ShieldTypeIntEnum,
    WeaponHandednessEnum,
)
from base.models import NPC
from base.models.abilities import Ability
from base.models.magic_items import (
    ArmsSlotItem,
    FeetSlotItem,
    HandsSlotItem,
    HeadSlotItem,
    MagicArmItemType,
    MagicArmorType,
    MagicItemType,
    NeckSlotItem,
    RingsSlotItem,
    SimpleMagicItem,
    WaistSlotItem,
)
from base.models.models import Weapon, WeaponType
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
                queryset=Power.objects.with_frequency_order()  # type: ignore
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
                'Двуручное оружие занимает обе руки, '
                'во второй руке не может быть другого оружия'
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

    def check_npc_without_paragon_path(self):
        if self.cleaned_data['is_bonus_applied'] and self.cleaned_data.get(
            'paragon_path'
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


class ParagonPathForm(forms.ModelForm):
    def clean(self) -> dict[str, Any] | None:
        if self.cleaned_data.get('klass') and self.cleaned_data.get('race'):
            message = 'Путь совершенства может быть либо классовым, либо расовым.'
            self.add_error('klass', message)
            self.add_error('race', message)
        return super().clean()


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


class MagicItemTypeFormBase(forms.ModelForm):

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена', initial=False
    )


class MagicItemTypeForm(MagicItemTypeFormBase):
    class Meta:
        model = MagicItemType
        fields = '__all__'


class MagicArmorTypeForm(MagicItemTypeFormBase):
    class Meta:
        model = MagicArmorType
        fields = '__all__'


class MagicArmItemTypeForm(MagicItemTypeFormBase):
    class Meta:
        model = MagicArmItemType
        fields = '__all__'
