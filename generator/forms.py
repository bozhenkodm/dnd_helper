from django import forms

from base.constants.constants import NPCRaceEnum
from base.models import Race
from generator.models import NPCName


class NPCNameForm(forms.ModelForm):
    class Meta:
        model = NPCName
        fields = '__all__'

    race = forms.ModelMultipleChoiceField(
        queryset=Race.objects.filter(is_sociable=True)
        .annotate(title=NPCRaceEnum.generate_case())
        .order_by('title'),
        widget=forms.CheckboxSelectMultiple,
        label='Раса',
    )
