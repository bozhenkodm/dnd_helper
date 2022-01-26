from django import forms

from base.models.encounters import EncounterParticipants


class EncounterChangeInitiativeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super().__init__(*args, **kwargs)
        self.fields['participant'] = forms.ModelChoiceField(
            queryset=EncounterParticipants.objects.filter(encounter__id=pk).ordered(),
            label='Участник',
            required=True,
        )
        self.fields['move_after'] = forms.ModelChoiceField(
            queryset=EncounterParticipants.objects.filter(encounter__id=pk).ordered(),
            label='Переместить после',
            required=True,
        )
