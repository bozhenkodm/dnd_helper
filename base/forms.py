from dataclasses import asdict

from django import forms
from multiselectfield import MultiSelectFormField

from base.constants.constants import AttributeEnum, SexEnum, SkillsEnum
from base.models import NPC
from base.models.models import Power


class NPCModelForm(forms.ModelForm):
    class Meta:
        model = NPC
        fields = '__all__'

    sex = forms.ChoiceField(
        choices=SexEnum.generate_choices(is_sorted=False), label='Пол'
    )

    def __init__(self, *args, **kwargs):
        super(NPCModelForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['var_bonus_attr'] = forms.ChoiceField(
                choices=[
                    (key.upper(), AttributeEnum[key.upper()].value)
                    for key, value in asdict(
                        self.instance.race_data_instance.var_ability_bonus
                    ).items()
                    if value
                ],
                label='Выборочный бонус характеристики',
            )
            choices = self.instance.klass_data_instance.trainable_skills
            self.fields['trained_skills'] = MultiSelectFormField(
                choices=(
                    (key.upper(), SkillsEnum[key.upper()].value)
                    for key, value in asdict(choices).items()
                    if value
                ),
                widget=forms.CheckboxSelectMultiple,
                label='Тренированный навыки',
            )
            self.fields['powers'] = forms.ModelMultipleChoiceField(
                queryset=Power.objects.with_frequency_order()
                .filter(klass=self.instance.klass, level__lte=self.instance.level)
                .order_by('level', 'frequency_order')
            )
