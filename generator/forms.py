from django import forms

from base.constants.constants import NPCRaceEnum, SexEnum
from base.models import Race
from generator.models import NPCName


class NPCNameForm(forms.ModelForm):
    class Meta:
        model = NPCName
        fields = '__all__'

    name_type = forms.ChoiceField(
        widget=forms.RadioSelect, label='Тип', choices=NPCName.NAMETYPE_CHOICES
    )
    sex = forms.ChoiceField(
        widget=forms.RadioSelect,
        label='Пол',
        choices=SexEnum.generate_choices(is_sorted=False),
    )
    race = forms.ModelMultipleChoiceField(
        queryset=Race.objects.filter(is_social=True)
        .annotate(title=NPCRaceEnum.generate_case())
        .order_by('title'),
        widget=forms.CheckboxSelectMultiple,
        label='Раса',
    )
