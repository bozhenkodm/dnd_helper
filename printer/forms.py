from django import forms

from printer.constants import ColorsStyle, Position
from printer.models import EncounterIcons, GridMap, Participant


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
    grid_color = forms.ChoiceField(
        label='Цвет грида',
        choices=ColorsStyle.generate_choices(),
        widget=forms.RadioSelect,
        initial=ColorsStyle.WHITE,
    )


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена'
    )  # TODO make mixin with this field
