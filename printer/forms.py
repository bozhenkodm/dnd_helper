from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from base.models.encounters import Encounter, PlayerCharacter
from base.models.models import NPC
from printer.constants import ColorStyle, Position, TransponseAction
from printer.models import Avatar, EncounterIcons, GridMap, ParticipantPlace, Zone


class EncounterIconForm(forms.ModelForm):
    class Meta:
        model = EncounterIcons
        fields = '__all__'

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена'
    )  # TODO make mixin with this field

    number_color = forms.ChoiceField(
        label='Цвет номера',
        choices=ColorStyle.generate_choices(),
        widget=forms.RadioSelect,
        initial=ColorStyle.RED,
    )
    number_position = forms.ChoiceField(
        label='Класс позиции номера на картинке',
        choices=Position.generate_choices(),
        widget=forms.RadioSelect,
        initial=Position.TOP_LEFT,
    )


class GridMapForm(forms.ModelForm):
    class Meta:
        model = GridMap
        fields = '__all__'

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена'
    )  # TODO make mixin with this field
    action = forms.TypedChoiceField(
        choices=TransponseAction.generate_choices(),
        label='Действие',
        widget=forms.RadioSelect,
        required=False,
        coerce=int,
    )
    grid_color = forms.ChoiceField(
        label='Цвет грида',
        choices=ColorStyle.generate_choices(),
        widget=forms.RadioSelect,
        initial=ColorStyle.WHITE,
    )
    encounter = forms.ModelChoiceField(
        queryset=Encounter.objects.filter(is_passed=False).order_by('-id'),
        required=False,
        label=_('Encounter'),
    )


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = '__all__'

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена'
    )  # TODO make mixin with this field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.npc:
            self.fields['npc'].queryset = NPC.objects.filter(
                Q(avatar__isnull=True) | Q(pk=self.instance.npc.id)
            )
        if self.instance and self.instance.pc:
            self.fields['pc'].queryset = PlayerCharacter.objects.filter(
                Q(avatar__isnull=True) | Q(pk=self.instance.pc.id)
            )


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена'
    )  # TODO make mixin with this field


# ---------------------- Views forms -------------------


class ParticipantPlaceForm(forms.ModelForm):
    class Meta:
        model = ParticipantPlace
        fields = ('id', 'row', 'col')
        widgets = {'id': forms.HiddenInput()}
