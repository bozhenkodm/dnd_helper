from django import forms

from base.models.encounters import PCParty
from printer.constants import ColorsStyle, Position, TransponseAction
from printer.models import EncounterIcons, GridMap, Participant, ParticipantPlace


class EncounterIconForm(forms.ModelForm):
    class Meta:
        model = EncounterIcons
        fields = '__all__'

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена'
    )  # TODO make mixin with this field

    number_color = forms.ChoiceField(
        label='Цвет номера',
        choices=ColorsStyle.generate_choices(),
        widget=forms.RadioSelect,
        initial=ColorsStyle.RED,
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
        choices=ColorsStyle.generate_choices(),
        widget=forms.RadioSelect,
        initial=ColorsStyle.WHITE,
    )
    party = forms.ModelChoiceField(queryset=PCParty.objects.all(), required=False)


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
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
