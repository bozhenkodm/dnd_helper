from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from base.models.encounters import Encounter, PlayerCharacter
from base.models.models import NPC
from printer.constants import ColorStyle, Position, TransponseAction
from printer.models import Avatar, EncounterIcons, GridMap, ParticipantPlace, Zone


class UploadFromClipboardForm(forms.ModelForm):
    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена'
    )


class EncounterIconForm(UploadFromClipboardForm):
    class Meta:
        model = EncounterIcons
        fields = '__all__'

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


class GridMapForm(UploadFromClipboardForm):
    class Meta:
        model = GridMap
        fields = '__all__'

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
    copy_from_map = forms.ModelChoiceField(
        queryset=GridMap.objects.all(),
        required=False,
        label=_('Copy from map'),
        help_text=_('Copy participants from another map'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['copy_from_map'].queryset = GridMap.objects.exclude(
                id=self.instance.id
            )


class ParticipantForm(UploadFromClipboardForm):
    class Meta:
        model = Avatar
        fields = '__all__'

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


class ZoneForm(UploadFromClipboardForm):
    class Meta:
        model = Zone
        fields = '__all__'


# ---------------------- Views forms -------------------


class ParticipantPlaceForm(forms.ModelForm):
    class Meta:
        model = ParticipantPlace
        fields = ('id', 'row', 'col')
        widgets = {'id': forms.HiddenInput()}
