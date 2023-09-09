from django import forms

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import SexEnum
from base.models import NPC


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
