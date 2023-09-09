from django import forms

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import SexEnum
from base.models import NPC
from base.models.magic_items import (
    ArmsSlotItem,
    FeetSlotItem,
    HandsSlotItem,
    HeadSlotItem,
    NeckSlotItem,
    RingsSlotItem,
    WaistSlotItem,
)
from base.models.models import Weapon
from base.objects.weapon_types import HolySymbol, KiFocus


class NPCModelForm(forms.ModelForm):
    class Meta:
        model = NPC
        fields = '__all__'

    sex = forms.ChoiceField(
        choices=SexEnum.generate_choices(is_sorted=False),
        label='Пол',
        widget=forms.RadioSelect,
    )

    subclass = forms.TypedChoiceField(
        coerce=int,
        choices=IntDescriptionSubclassEnum.generate_choices(),
        label='Подкласс',
        show_hidden_initial=True,
    )
    no_hand = forms.ModelChoiceField(
        queryset=Weapon.objects.select_related('weapon_type', 'magic_item_type')
        .filter(
            weapon_type__slug__in=(KiFocus.slug(), HolySymbol.slug())
            # TODO make it type, put it in database and filter by it
        )
        .order_by('level', 'weapon_type__name', 'magic_item_type__name'),
        label='Инструмент не в руку',
        required=False,
    )
    neck_slot = forms.ModelChoiceField(
        queryset=NeckSlotItem.objects.select_related('magic_item_type').filter(
            magic_item_type__slots__contains=NeckSlotItem.SLOT.value
        ),
        label='Предмет на шею',
        required=False,
    )
    head_slot = forms.ModelChoiceField(
        queryset=HeadSlotItem.objects.select_related('magic_item_type').filter(
            magic_item_type__slots__contains=HeadSlotItem.SLOT.value
        ),
        label='Предмет на голову',
        required=False,
    )
    waist_slot = forms.ModelChoiceField(
        queryset=WaistSlotItem.objects.select_related('magic_item_type').filter(
            magic_item_type__slots__contains=WaistSlotItem.SLOT.value
        ),
        label='Предмет на пояс',
        required=False,
    )
    feet_slot = forms.ModelChoiceField(
        queryset=FeetSlotItem.objects.select_related('magic_item_type').filter(
            magic_item_type__slots__contains=FeetSlotItem.SLOT.value
        ),
        label='Предмет на ноги',
        required=False,
    )
    arms_slot = forms.ModelChoiceField(
        queryset=ArmsSlotItem.objects.select_related('magic_item_type').filter(
            magic_item_type__slots__contains=ArmsSlotItem.SLOT.value
        ),
        label='Предмет на предплечья',
        required=False,
    )

    left_ring_slot = forms.ModelChoiceField(
        queryset=RingsSlotItem.objects.select_related('magic_item_type').filter(
            magic_item_type__slots__contains=RingsSlotItem.SLOT.value
        ),
        label='Кольцо на левую руку',
        required=False,
    )

    right_ring_slot = forms.ModelChoiceField(
        queryset=RingsSlotItem.objects.select_related('magic_item_type').filter(
            magic_item_type__slots__contains=RingsSlotItem.SLOT.value
        ),
        label='Кольцо на правую руку',
        required=False,
    )
    gloves_slot = forms.ModelChoiceField(
        queryset=HandsSlotItem.objects.select_related('magic_item_type').filter(
            magic_item_type__slots__contains=HandsSlotItem.SLOT.value
        ),
        label='Предмет на кисти',
        required=False,
    )
