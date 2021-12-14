from dataclasses import asdict

from django import forms
from multiselectfield import MultiSelectFormField

from base.constants.constants import AttributeEnum, NPCClassIntEnum, SexEnum, SkillsEnum
from base.models import NPC
from base.models.models import Armor, Class, Power, Weapon, WeaponType
from base.objects import weapon_types_tuple


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
            if subclass_enum := getattr(
                self.instance.klass_data_instance, 'SubclassEnum', None
            ):
                self.fields['subclass'] = forms.ChoiceField(
                    choices=subclass_enum.generate_choices(), label='Подкласс'
                )


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.id:
            existing_classes = set(
                self._meta.model.objects.values_list('name', flat=True)
            )
            self.fields['name'] = forms.ChoiceField(
                choices=[
                    item
                    for item in NPCClassIntEnum.generate_choices()
                    if item[0] not in existing_classes
                ],
                label='Название класса',
            )


class WeaponTypeForm(forms.ModelForm):
    class Meta:
        model = WeaponType
        fields = '__all__'

    slug = forms.ChoiceField(
        choices=[
            (cls.slug, f'{cls.name}')
            for cls in weapon_types_tuple
            if cls.slug not in set(WeaponType.objects.values_list('slug', flat=True))
        ],
        label='Название',
    )


class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id and self.instance.magic_item:
            self.fields['level'] = forms.ChoiceField(
                choices=(
                    (i, i)
                    for i in range(
                        self.instance.magic_item.min_level,
                        31,
                        self.instance.magic_item.step,
                    )
                ),
                label='Уровень',
            )


class ArmorForm(forms.ModelForm):
    class Meta:
        model = Armor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArmorForm, self).__init__(*args, **kwargs)
        if self.instance.id and self.instance.magic_item:
            self.fields['level'] = forms.ChoiceField(
                choices=(
                    (i, i)
                    for i in range(
                        self.instance.magic_item.min_level,
                        31,
                        self.instance.magic_item.step,
                    )
                ),
                label='Уровень',
            )
