from itertools import chain
from typing import Any, cast

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    LEVELS_WITH_ABILITY_BONUS,
    DiceIntEnum,
    MagicItemSlot,
    NPCClassEnum,
    NPCOtherProperties,
    NPCRaceEnum,
    PowerSourceIntEnum,
    SexEnum,
)
from base.models.abilities import Ability
from base.models.condition import Condition, Constraint, PropertiesCondition
from base.models.feats import Feat
from base.models.items import (
    Armor,
    ArmsSlotItem,
    BaseArmorType,
    FeetSlotItem,
    HandsSlotItem,
    HeadSlotItem,
    MagicArmItemType,
    MagicArmorType,
    MagicItemType,
    MagicWeaponType,
    NeckSlotItem,
    RingsSlotItem,
    ShieldType,
    SimpleMagicItem,
    WaistSlotItem,
    Weapon,
    WeaponCategory,
    WeaponType,
)
from base.models.klass import Class, Subclass
from base.models.models import NPC, ParagonPath, Race
from base.models.powers import Effect, Power
from base.models.skills import Skill


class NPCModelForm(forms.ModelForm):
    class Meta:
        model = NPC
        fields = '__all__'

    level4_abilities_bonus = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Бонус характеристики на 4 уровне',
        required=False,
    )
    level8_abilities_bonus = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Бонус характеристики на 8 уровне',
        required=False,
    )
    level14_abilities_bonus = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Бонус характеристики на 14 уровне',
        required=False,
    )
    level18_abilities_bonus = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Бонус характеристики на 18 уровне',
        required=False,
    )
    level24_abilities_bonus = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Бонус характеристики на 24 уровне',
        required=False,
    )
    level28_abilities_bonus = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Бонус характеристики на 28 уровне',
        required=False,
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.instance: NPC
            self.fields['var_bonus_ability'].queryset = Ability.objects.filter(
                races=self.instance.race
            )
            self.fields['var_bonus_ability'].required = Ability.objects.filter(
                races=self.instance.race
            ).exists()

            for level in LEVELS_WITH_ABILITY_BONUS:
                if level > self.instance.level:
                    break
                self.fields[f'level{level}_abilities_bonus'].initial = (
                    Ability.objects.filter(
                        level_bonuses__npc=self.instance, level_bonuses__level=level
                    )
                )

            self.fields['trained_skills'] = forms.ModelMultipleChoiceField(
                queryset=Skill.objects.filter(classes=self.instance.klass),
                widget=forms.CheckboxSelectMultiple,
                label=_('Trained skills'),
                required=False,
            )
            if not self.instance.is_bonus_applied:
                if self.instance.level >= 11:
                    self.fields['paragon_path'].queryset = ParagonPath.objects.filter(
                        id__in=ParagonPath.get_ids_for_npc(
                            self.instance,
                            initial_query=models.Q(klass=self.instance.klass)
                            | models.Q(race=self.instance.race),
                        ),
                    )
                self.fields['feats'].queryset = Feat.objects.filter(
                    id__in=Feat.get_ids_for_npc(
                        self.instance,
                        initial_query=models.Q(min_level__lte=self.instance.level),
                    ),
                ).order_by('min_level', 'name')
            self.fields['powers'].queryset = (
                Power.objects.order_by('frequency')
                .filter(
                    models.Q(klass=self.instance.klass)
                    | models.Q(race=self.instance.race, level__gt=0)
                    | models.Q(skill__classes_for_mandatory=self.instance.klass)
                    | models.Q(skill__npcs=self.instance),
                    level__lte=self.instance.level,
                )
                .exclude(classes=self.instance.klass)
                .exclude(subclasses__klass=self.instance.klass)
                .order_by('level', 'frequency')
            )
            self.fields['subclass_id'] = forms.ChoiceField(
                choices=self.instance.klass.subclasses.generate_choices(),
                label='Подкласс',
            )

            # TODO doesn't work
            self.fields['armor'].queryset = Armor.objects.select_related(
                'armor_type', 'armor_type__base_armor_type'
            ).filter(
                armor_type__base_armor_type__in=self.instance.available_armor_types
            )

            self.fields['neck_slot'].queryset = NeckSlotItem.objects.select_related(
                'magic_item_type'
            ).filter(magic_item_type__slot=NeckSlotItem.SLOT.value)
            self.fields['head_slot'].queryset = HeadSlotItem.objects.select_related(
                'magic_item_type'
            ).filter(magic_item_type__slot=HeadSlotItem.SLOT.value)
            self.fields['waist_slot'].queryset = WaistSlotItem.objects.select_related(
                'magic_item_type'
            ).filter(magic_item_type__slot=WaistSlotItem.SLOT.value)
            self.fields['feet_slot'].queryset = FeetSlotItem.objects.select_related(
                'magic_item_type'
            ).filter(magic_item_type__slot=FeetSlotItem.SLOT.value)
            self.fields['arms_slot'].queryset = (
                ArmsSlotItem.objects.select_related('magic_item_type')
                .filter(
                    models.Q(magic_item_type__slot=ArmsSlotItem.SLOT.value)
                    & (
                        models.Q(shield_type__in=self.instance.klass.shields.all())
                        | models.Q(shield_type__in=self.instance.subclass.shields.all())
                        | models.Q(shield_type__isnull=True)
                    ),
                )
                .order_by('magic_item_type__name', 'shield_type__base_shield_type')
            )
            self.fields['left_ring_slot'].queryset = (
                RingsSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slot=RingsSlotItem.SLOT.value
                )
            )
            self.fields['right_ring_slot'].queryset = (
                RingsSlotItem.objects.select_related('magic_item_type').filter(
                    magic_item_type__slot=RingsSlotItem.SLOT.value
                )
            )
            self.fields['gloves_slot'].queryset = HandsSlotItem.objects.select_related(
                'magic_item_type'
            ).filter(magic_item_type__slot=HandsSlotItem.SLOT.value)

    def add_errors(self, *fields, error=''):
        for field in fields:
            self.add_error(field, ValidationError(error))

    def check_shield_and_weapon_in_one_hand(
        self, secondary_hand, shield_is_in_hand: bool
    ) -> None:
        if secondary_hand and shield_is_in_hand:
            self.add_errors(
                'arms_slot',
                'secondary_hand',
                'Нельзя удержать в одной руке оружие и щит',
            )

    def check_two_handed_weapon_held_with_two_hands(
        self, primary_hand, secondary_hand, shield_is_in_hand: bool
    ) -> None:
        if primary_hand and primary_hand.handedness.is_two_handed:
            error = ValidationError(
                'Двуручное оружие занимает обе руки, '
                'во второй руке не может быть другого предмета'
            )
            if secondary_hand:
                self.add_error('secondary_hand', error)
            if shield_is_in_hand:
                self.add_error('arms_slot', error)

    def check_two_weapons_in_two_hands(self, primary_hand, secondary_hand) -> None:
        if not secondary_hand:
            return
        if not primary_hand:
            self.add_errors(
                'primary_hand', 'secondary_hand', error='Сначала занимаем основную руку'
            )
        if primary_hand.is_double:
            self.add_errors(
                'primary_hand',
                'secondary_hand',
                error='Двойное оружие занимает две руки',
            )
        if primary_hand.handedness.is_one_handed:
            if secondary_hand.handedness.is_off_hand:
                return
            if secondary_hand.handedness.is_two_handed or secondary_hand.is_double:
                self.add_errors(
                    'primary_hand',
                    'secondary_hand',
                    error='Двойное и двуручное оружие занимает две руки',
                )
                return
            subclass_slug = self.instance.klass.subclasses.get(
                subclass_id=self.cleaned_data['subclass_id']
            ).slug
            can_wield_two_one_handed_weapons = (
                self.instance.klass.name == NPCClassEnum.RANGER
                and subclass_slug == 'TWO_HANDED'
                or self.instance.klass.name == NPCClassEnum.BARBARIAN
                and subclass_slug == 'WHIRLING'
            )
            if (
                can_wield_two_one_handed_weapons
                and secondary_hand.handedness.is_two_handed
            ):
                self.add_error(
                    'secondary_hand',
                    ValidationError(
                        'Даже следопыты и варвары '
                        'не могут держать двуручное оружие во второй руке'
                    ),
                )
            elif (
                not can_wield_two_one_handed_weapons
                and not secondary_hand.handedness.is_off_hand
            ):
                self.add_error(
                    'secondary_hand',
                    ValidationError(
                        'Во второй руке можно держать только дополнительное оружие'
                    ),
                )

    def check_double_weapon(
        self, primary_hand, secondary_hand, shield_is_in_hand: bool
    ):
        if secondary_hand and hasattr(secondary_hand.weapon_type, 'secondary_end'):
            self.add_error(
                'secondary_hand',
                ValidationError('Двойное оружие должно располагаться в основной руке'),
            )
        if (
            primary_hand
            and hasattr(primary_hand.weapon_type, 'secondary_end')
            and (secondary_hand or shield_is_in_hand)
        ):
            message = 'Для двойного оружия должна быть свободна вторая рука'
            self.add_error('primary_hand', ValidationError(message))
            if secondary_hand:
                self.add_error('secondary_hand', ValidationError(message))
            if shield_is_in_hand:
                self.add_error('arms_slot', ValidationError(message))

    def check_proper_sex(self) -> None:
        if 'race' in self.cleaned_data:
            if (
                self.cleaned_data['race'].name == NPCRaceEnum.HAMADRYAD
                and self.cleaned_data['sex'] != SexEnum.F
            ):
                self.add_errors('sex', 'race', 'Гамадриады только женщины')

            if (
                self.cleaned_data['race'].name == NPCRaceEnum.SATYR
                and self.cleaned_data['sex'] != SexEnum.M
            ):
                self.add_errors('sex', 'race', 'Сатиры только мужчины')

    def check_npc_without_paragon_path(self):
        if self.cleaned_data['is_bonus_applied'] and self.cleaned_data.get(
            'paragon_path'
        ):
            message = (
                'Неигровые персонажи c бонусом уровня '
                'не могут иметь путь совершенства'
            )
            self.add_errors('paragon_path', 'is_bonus_applied', message)

    def clean(self) -> dict[str, Any] | None:
        cast(NPC, self.instance)
        if not self.instance.id:
            return super().clean()
        self.check_npc_without_paragon_path()
        primary_hand = self.cleaned_data.get('primary_hand')
        secondary_hand = self.cleaned_data.get('secondary_hand')
        shield_is_in_hand = bool(
            self.cleaned_data['arms_slot']
            and self.cleaned_data['arms_slot'].shield_type
        )
        self.check_shield_and_weapon_in_one_hand(secondary_hand, shield_is_in_hand)
        self.check_two_handed_weapon_held_with_two_hands(
            primary_hand, secondary_hand, shield_is_in_hand
        )
        self.check_two_weapons_in_two_hands(primary_hand, secondary_hand)
        self.check_double_weapon(primary_hand, secondary_hand, shield_is_in_hand)

        return super().clean()


class ClassAbstractForm(forms.ModelForm):
    armor_types = forms.ModelMultipleChoiceField(
        queryset=BaseArmorType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_('Available armor types'),
        required=True,
    )
    shields = forms.ModelMultipleChoiceField(
        queryset=ShieldType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_('Available shields'),
        required=False,
    )


class ClassForm(ClassAbstractForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.instance: Class
            self.fields['default_powers'].queryset = Power.objects.filter(
                klass=self.instance
            ).order_by('level', 'name')


class SubclassForm(ClassAbstractForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.instance: Subclass
            self.fields['default_powers'].queryset = Power.objects.filter(
                klass=self.instance.klass
            ).order_by('level', 'name')


class ParagonPathForm(forms.ModelForm):
    def clean(self) -> dict[str, Any] | None:
        if self.cleaned_data.get('klass') and self.cleaned_data.get('race'):
            message = 'Путь совершенства может быть либо классовым, либо расовым.'
            self.add_error('klass', message)
            self.add_error('race', message)
        return super().clean()


class ItemAbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.magic_item_type:
            self.fields['level'] = forms.ChoiceField(
                choices=((i, i) for i in self.instance.magic_item_type.level_range()),
                label=_('Level'),
            )


class WeaponForm(ItemAbstractForm):
    class Meta:
        model = Weapon
        fields = '__all__'


class MagicItemForm(ItemAbstractForm):
    class Meta:
        model = SimpleMagicItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['magic_item_type'].required = True


class ArmsSlotItemForm(ItemAbstractForm):
    class Meta:
        model = ArmsSlotItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['magic_item_type'].queryset = MagicItemType.objects.filter(
            slot=MagicItemSlot.ARMS.value
        )


class MagicItemTypeFormBase(forms.ModelForm):
    upload_from_clipboard = forms.BooleanField(
        required=False, label='Загрузить из буфера обмена', initial=False
    )


class MagicItemTypeForm(MagicItemTypeFormBase):
    class Meta:
        model = MagicItemType
        fields = '__all__'


class MagicArmorTypeForm(MagicItemTypeFormBase):
    class Meta:
        model = MagicArmorType
        fields = '__all__'


class MagicArmItemTypeForm(MagicItemTypeFormBase):
    class Meta:
        model = MagicArmItemType
        fields = '__all__'


class MagicWeaponTypeForm(MagicItemTypeFormBase):
    class Meta:
        model = MagicWeaponType
        fields = '__all__'


class ConstraintForm(forms.ModelForm):
    class Meta:
        model = Constraint
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id and self.instance.content_type:
            self.fields['object_id'] = forms.ChoiceField(
                choices=(
                    (item.id, str(item))
                    for item in self.instance.content_type.model_class().objects.all()
                ),
                label=str(self.instance.content_type).split('|')[1].strip(),
            )


class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id and self.instance.content_type:
            model_class = self.instance.content_type.model_class()
            self.fields['object_id'] = forms.ChoiceField(
                choices=chain(
                    ((0, '---------'),),
                    ((item.id, str(item)) for item in model_class.objects.all()),
                ),
                label=str(self.instance.content_type).split('|')[1].strip(),
            )


class PropertiesConditionForm(forms.ModelForm):
    class Meta:
        model = PropertiesCondition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id and self.instance.type == NPCOtherProperties.POWER_SOURCE:
            self.fields['value'] = forms.TypedChoiceField(
                choices=PowerSourceIntEnum.generate_choices(zero_item=(0, '---------')),
                label=_('Value'),
                coerce=int,
            )


class FeatForm(forms.ModelForm):
    class Meta:
        model = Feat
        fields = '__all__'

    race = forms.ModelChoiceField(
        queryset=Race.objects.order_by('-is_social', 'name_display'),
        required=False,
        label=_('Race'),
    )
    klass = forms.ModelChoiceField(
        queryset=Class.objects.all(), required=False, label=_('Class')
    )
    subclass = forms.ModelChoiceField(
        queryset=Subclass.objects.filter(subclass_id__gt=0),
        required=False,
        label=_('Subclass'),
    )
    feat = forms.ModelChoiceField(
        queryset=Feat.objects.all(), required=False, label=_('Feat')
    )
    trained_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        label=_('Trained skills'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'radiolist inline'}),
    )

    strength = forms.IntegerField(required=False, label=_('Strength'))
    constitution = forms.IntegerField(required=False, label=_('Constitution'))
    dexterity = forms.IntegerField(required=False, label=_('Dexterity'))
    intelligence = forms.IntegerField(required=False, label=_('Intelligence'))
    wisdom = forms.IntegerField(required=False, label=_('Wisdom'))
    charisma = forms.IntegerField(required=False, label=_('Charisma'))
    power_source = forms.TypedChoiceField(
        choices=PowerSourceIntEnum.generate_choices(zero_item=(0, '-------')),
        coerce=int,
        label=_('Power source'),
        required=False,
    )

    weapon_categories = forms.ModelMultipleChoiceField(
        queryset=WeaponCategory.objects.all(),
        required=False,
        label=_('Weapon categories'),
    )
    weapon_types = forms.ModelMultipleChoiceField(
        queryset=WeaponType.objects.filter(primary_end__isnull=True).order_by('name'),
        required=False,
        label=_('Weapon types'),
    )
    armor_types = forms.ModelMultipleChoiceField(
        queryset=BaseArmorType.objects.all(), required=False, label=_('Armor types')
    )
    shields = forms.ModelMultipleChoiceField(
        queryset=ShieldType.objects.all(),
        required=False,
        label=_('Shield types'),
    )


class PowerForm(forms.ModelForm):
    class Meta:
        model = Power
        fields = '__all__'

    effects = forms.ModelMultipleChoiceField(
        queryset=Effect.objects.filter(is_damage=False),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('Effects'),
    )
    damage_types = forms.ModelMultipleChoiceField(
        queryset=Effect.objects.filter(is_damage=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('Damage type'),
    )
