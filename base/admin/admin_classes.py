import io
import re
import subprocess
import textwrap
import typing
import urllib.parse
from functools import reduce

from django import forms
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.files.images import ImageFile
from django.db import models
from django.db.transaction import atomic
from django.forms import CheckboxSelectMultiple
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from base.admin.base_admin_classes import TextFromImage
from base.admin.forms import (
    ArmsSlotItemForm,
    ClassForm,
    ConditionForm,
    ConstraintForm,
    FeatForm,
    MagicArmItemTypeForm,
    MagicArmorTypeForm,
    MagicItemForm,
    MagicItemTypeForm,
    MagicWeaponTypeForm,
    MonsterForm,
    NPCModelForm,
    ParagonPathForm,
    ParagonPathPowerForm,
    PowerForm,
    PropertiesConditionForm,
    SubclassForm,
    WeaponForm,
)
from base.constants.constants import (
    LEVELS_WITH_ABILITY_BONUS,
    AccessoryTypeEnum,
    ArmorTypeIntEnum,
    BonusSource,
    MagicItemSlot,
    PowerFrequencyIntEnum,
    PowerPropertyTitle,
    SizeIntEnum,
    WeaponGroupEnum,
)
from base.models.abilities import AbilityLevelBonus
from base.models.bonuses import Bonus
from base.models.condition import (
    AvailabilityCondition,
    Condition,
    Constraint,
    PropertiesCondition,
)
from base.models.encounters import CombatantMonster, CombatantPC
from base.models.feats import ItemState
from base.models.items import (
    Armor,
    ArmorType,
    ArmsSlotItem,
    MagicArmorType,
    MagicItemType,
    MagicWeaponType,
    ShieldType,
    SimpleMagicItem,
    Weapon,
    WeaponType,
)
from base.models.models import NPC
from base.models.powers import Power, PowerProperty


class PowerReadonlyInline(admin.TabularInline):
    model = Power
    fields = ('name', 'power_text')
    readonly_fields = fields

    @admin.display(description='Текст таланта')
    def power_text(self, obj) -> str:
        if not obj.id:
            return '-'
        return obj.text

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class ConstraintInline(GenericTabularInline):
    model = Constraint
    show_change_link = True
    extra = 1


class BonusInline(admin.TabularInline):
    model = Bonus
    fields = ('bonus_type', 'value', 'source')
    show_change_link = True


@admin.action(description='Социализировать расы')
def make_sociable(modeladmin, request, queryset) -> None:
    queryset.update(is_social=True)


@admin.action(description='Десоциализировать расы')
def make_unsociable(modeladmin, request, queryset) -> None:
    queryset.update(is_social=False)


class RaceAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'const_ability_bonus',
        'var_ability_bonus',
        'speed',
        'vision',
        'size',
        'weapon_types',
        'is_social',
    )
    list_filter = (
        'speed',
        'vision',
        'size',
        'is_social',
    )
    list_display = ('name_display', 'speed', 'vision', 'size', 'is_social')
    search_fields = ('name_display',)
    actions = (make_sociable, make_unsociable)
    inlines = (
        BonusInline,
        PowerReadonlyInline,
    )

    def get_readonly_fields(self, request, obj=None) -> tuple:
        if obj and obj.id:
            return (
                'name',
                'const_ability_bonus',
                'var_ability_bonus',
                'speed',
                'vision',
                'size',
            )
        return ()

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if formset.model == Bonus:
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.source = BonusSource.RACE
                    instance.name = (
                        f'{form.instance}: {instance.get_bonus_type_display()}'
                    )
                    instance.save()


class ClassAdmin(admin.ModelAdmin):
    search_fields = ('name_display',)
    ordering = ('name_display',)
    readonly_fields = (
        'available_weapons',
        'implement_types',
        'mandatory_skills',
        'trainable_skills',
        'power_source',
        'role',
    )
    fields = (
        (
            'armor_types',
            'shields',
        ),
        (
            'available_weapons',
            'implement_types',
        ),
        (
            'mandatory_skills',
            'trainable_skills',
        ),
        (
            'power_source',
            'role',
        ),
        (
            'default_feats',
            'default_powers',
        ),
        (
            'fortitude',
            'reflex',
            'will',
        ),
        'book_source',
    )
    autocomplete_fields = ('default_feats',)
    list_filter = ('power_source', 'role')
    list_display = ('name_display',)
    inlines = (BonusInline,)
    form = ClassForm

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    # def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    @admin.display(description='Владение оружием')
    def available_weapons(self, obj):
        if not obj.id:
            return '-'
        try:
            return ', '.join(
                [str(wc) for wc in obj.weapon_categories.all()]
                + [weapon_type.name for weapon_type in obj.weapon_types.all()]
            )
        except TypeError:
            return '-'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if formset.model == Bonus:
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.source = BonusSource.CLASS
                    instance.name = (
                        f'{form.instance}: {instance.get_bonus_type_display()}'
                    )
                    instance.save()


class SubclassAdmin(admin.ModelAdmin):
    ordering = ('klass__name_display', 'subclass_id', 'name')
    list_filter = ('klass',)
    list_display = ('__str__', 'klass')
    autocomplete_fields = ('default_feats',)
    inlines = (BonusInline,)
    form = SubclassForm
    readonly_fields = ('available_weapons',)
    fields = (
        (
            'name',
            'slug',
            'subclass_id',
        ),
        'klass',
        (
            'armor_types',
            'shields',
        ),
        (
            'available_weapons',
            'implement_types',
        ),
        (
            'default_feats',
            'default_powers',
        ),
        'book_source',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(subclass_id=0)

    @admin.display(description='Владение оружием')
    def available_weapons(self, obj):
        if not obj.id:
            return '-'
        try:
            return ', '.join(
                [str(wc) for wc in obj.weapon_categories.all()]
                + [weapon_type.name for weapon_type in obj.weapon_types.all()]
            )
        except TypeError:
            return '-'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if formset.model == Bonus:
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.source = BonusSource.CLASS
                    instance.name = (
                        f'{form.instance}: {instance.get_bonus_type_display()}'
                    )
                    instance.save()


class ParagonPathAdmin(admin.ModelAdmin):
    inlines = (
        ConstraintInline,
        PowerReadonlyInline,
    )
    form = ParagonPathForm


@admin.action(description='Кэшировать')
def cache_npc(modeladmin, request, queryset):
    for npc in queryset:
        npc.cache_all()


class NPCAdmin(admin.ModelAdmin):
    fields = [
        (
            'name',
            'avatar_img',
            'sex',
        ),
        'is_bonus_applied',
        (
            'race',
            'functional_template',
        ),
        (
            'klass',
            'subclass_id',
        ),
        ('level', 'experience'),
        'description',
        (
            'base_strength',
            'base_constitution',
            'base_dexterity',
        ),
        (
            'base_intelligence',
            'base_wisdom',
            'base_charisma',
        ),
        (
            'const_bonus_ability',
            'var_bonus_ability',
        ),
        'mandatory_skills',
        'trained_skills',
        (
            'armor',
            'arms_slot',
        ),
        'primary_hand',
        'secondary_hand',
        'no_hand',
        (
            'neck_slot',
            'head_slot',
        ),
        (
            'waist_slot',
            'feet_slot',
            'gloves_slot',
        ),
        (
            'left_ring_slot',
            'right_ring_slot',
        ),
        'powers',
    ]
    autocomplete_fields = (
        'race',
        'klass',
        'trained_weapons',
        'primary_hand',
        'secondary_hand',
        'no_hand',
        'armor',
    )
    filter_horizontal = ('powers', 'feats')
    search_fields = ('name',)
    list_filter = (
        ('klass', admin.RelatedOnlyFieldListFilter),
        ('race', admin.RelatedOnlyFieldListFilter),
        ('functional_template', admin.RelatedOnlyFieldListFilter),
        ('paragon_path', admin.RelatedOnlyFieldListFilter),
        'sex',
        ('avatar', admin.EmptyFieldListFilter),  # TODO change to simple list filter
    )
    list_display = (
        'name',
        'level',
        'race',
        'klass',
        'paragon_path',
        'functional_template',
    )
    radio_fields = {'sex': admin.VERTICAL, 'var_bonus_ability': admin.VERTICAL}
    list_per_page = 20
    form = NPCModelForm
    actions = (cache_npc,)

    def get_queryset(self, request: HttpRequest) -> models.QuerySet:
        qs = super().get_queryset(request)
        query = models.Q(owner=request.user)
        if request.user.is_superuser:
            query |= models.Q(owner__isnull=True)
        qs.filter(query)
        return qs

    def has_view_or_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if obj is None:
            return super().has_view_or_change_permission(request, obj)
        if request.user.is_superuser and obj.owner is None:
            return True
        if request.user == obj.owner:
            return True
        return False

    def get_object(self, request, object_id, from_field=None):
        self.object = super().get_object(request, object_id, from_field)
        typing.cast(NPC, self.object)
        return self.object

    def _get_level_abilities_bonus_fields(self, obj) -> list[str]:
        result = []
        for level in LEVELS_WITH_ABILITY_BONUS:
            if not obj or obj.level < level:
                break
            result.append(f'level{level}_abilities_bonus')
        return result

    def get_fields(self, request: HttpRequest, obj=None):
        if not obj:
            return (
                (
                    'name',
                    'sex',
                ),
                'description',
                'is_bonus_applied',
                (
                    'race',
                    'klass',
                ),
                'level',
                (
                    'base_strength',
                    'base_constitution',
                    'base_dexterity',
                ),
                (
                    'base_intelligence',
                    'base_wisdom',
                    'base_charisma',
                ),
            )
        result = self.fields[:]
        if not obj.is_bonus_applied:
            result[2] = (
                'race',
                'paragon_path',
            )
        index_to_insert = result.index('mandatory_skills')
        result.insert(index_to_insert, self._get_level_abilities_bonus_fields(obj))
        if not obj.is_bonus_applied:
            result.extend(
                [
                    'trained_weapons',
                    'feats',
                ]
            )
        return result

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['mandatory_skills', 'avatar_img', 'const_bonus_ability']
        if obj and obj.level < 11:
            readonly_fields.append('paragon_path')
        return readonly_fields

    @admin.display(description='Тренированные навыки')
    def mandatory_skills(self, obj):
        return ', '.join(str(s) for s in obj.klass.mandatory_skills.all())

    @admin.display(description='Аватар')
    def avatar_img(self, obj):
        if not obj.avatar:
            return '-'
        return mark_safe(
            f'<a href="{obj.avatar.admin_edit_url}" target="blank">'
            f'<img width=50px; height=auto; src="{obj.avatar.base_image.url}" '
            f'alt="Аватар недоступен"/></a>'
        )

    @admin.display(description='Постоянный бонус характеристики')
    def const_bonus_ability(self, obj):
        if not obj.id or not obj.race.const_ability_bonus.all():
            return '-'
        return ', '.join(str(ability) for ability in obj.race.const_ability_bonus.all())

    @atomic
    def save_model(self, request, obj, form, change):
        # we remove all default powers on model save
        # to add it during save related
        if obj.id:
            for power in obj.powers.filter(level=0):
                obj.powers.remove(power)
        if change:
            obj.level = max(
                obj.level_by_experience(form.cleaned_data['experience']), obj.level
            )
            obj.experience = max(
                obj.experience_by_level(form.cleaned_data['level']), obj.experience
            )
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        if not change:
            super().save_related(request, form, formsets, change)
            return
        ability_bonuses = []
        npc = form.instance
        for level in LEVELS_WITH_ABILITY_BONUS:
            if level > npc.level:
                break
            for ability in form.cleaned_data[f'level{level}_abilities_bonus']:
                if not AbilityLevelBonus.objects.filter(
                    npc=npc, level=level, ability=ability
                ).exists():
                    ability_bonuses.append(
                        AbilityLevelBonus(npc=npc, level=level, ability=ability)
                    )
        AbilityLevelBonus.objects.bulk_create(ability_bonuses)
        super().save_related(request, form, formsets, change)
        npc.cache_all()


class CombatantsMonsterInlineAdmin(admin.TabularInline):
    model = CombatantMonster

    def get_extra(self, request, obj=None, **kwargs):
        if not obj:
            return self.extra
        return 0


class CombatantsPCSInlineAdmin(admin.TabularInline):
    model = CombatantPC

    def get_extra(self, request, obj=None, **kwargs):
        if not obj:
            return self.extra
        return 0


@admin.action(description='Отметить пройденной')
def make_passed(modeladmin, request, queryset):
    queryset.update(is_passed=True)


class EncounterAdmin(admin.ModelAdmin):
    fields = (
        'short_description',
        'roll_for_players',
        'party',
        ('npcs', 'npc_links'),
        'encounter_link',
        'is_passed',
    )
    readonly_fields = ('encounter_link', 'npc_links')
    inlines = (
        CombatantsPCSInlineAdmin,
        CombatantsMonsterInlineAdmin,
    )
    autocomplete_fields = ('npcs',)
    list_filter = ('is_passed',)
    list_per_page = 5
    actions = (make_passed,)

    @admin.display(description='Страница сцены')
    def encounter_link(self, obj):
        if not obj.id:
            return '-'
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    @admin.display(description='Страницы персонажей')
    def npc_links(self, obj):
        if not obj.npcs.exists():
            return '-'
        return mark_safe(
            '<br>'.join(
                f'<a href="{npc.url}" target="_blank">{npc}</a>'
                for npc in obj.npcs.all()
            )
        )

    @atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.roll_initiative()


class ArmorTypeAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'base_armor_type',
        'bonus_armor_class',
        'minimal_enhancement',
        'armor_class',
        'speed_penalty',
        'skill_penalty',
        'fortitude_bonus',
        'reflex_bonus',
        'will_bonus',
        'book_source',
    )
    readonly_fields = ('armor_class',)
    list_display = ('__str__', 'base_armor_type')
    ordering = ('base_armor_type', 'minimal_enhancement')

    @admin.display(description='Класс доспеха')
    def armor_class(self, obj):
        if not obj.id:
            return '-'
        return obj.armor_class

    @atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            return
        for magic_armor_type in MagicArmorType.objects.filter(
            armor_type_slots=obj.base_armor_type
        ):
            for level in magic_armor_type.level_range():
                Armor.create_on_base(obj, magic_armor_type, level)


class ArmorAdmin(admin.ModelAdmin):
    fields = (
        'armor_type',
        'magic_item_type',
        'level',
    )
    ordering = ('level', 'armor_type__base_armor_type')
    readonly_fields = ('armor_class',)
    search_fields = (
        'armor_type__name',
        'displayed_name',
        'magic_item_type__name',
        'enhancement',
    )

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'magic_item_type':
            kwargs['queryset'] = MagicItemType.objects.filter(
                slot=MagicItemSlot.ARMOR.value
            ).order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .with_enhancement()
            .annotate(
                displayed_name=ArmorTypeIntEnum.generate_value_description_case(
                    field='armor_type__base_armor_type__armor_class'
                ),
            )
        )


class WeaponTypeAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'category', 'handedness')
    search_fields = ('name',)
    readonly_fields = (
        'prof_bonus',
        'damage',
        'properties',
    )
    list_filter = ('handedness', 'category')
    save_as = True

    def get_fields(self, request, obj=None):
        if obj and obj.id:
            return (
                'category',
                'groups',
                'prof_bonus',
                'damage',
                'handedness',
                'properties',
                'primary_end',
                'book_source',
            )
        return (
            'slug',
            'category',
            'groups',
            'prof_bonus',
            'damage',
            'handedness',
            'primary_end',
            'book_source',
        )

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if self.model._meta.app_label == 'base':
            return {}

        return super().get_model_perms(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    # def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    @admin.display(description='Свойства оружия')
    def properties(self, obj):
        if not obj.id:
            return '-'
        return obj.properties_text

    @admin.display(description='Урон')
    def damage(self, obj):
        if not obj.id:
            return '-'
        return obj.damage()

    @atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            return
        queries = [
            models.Q(weapon_type__id=obj.pk),
            models.Q(weapon_categories__id=obj.category.pk),
            models.Q(weapon_groups__id__in=obj.groups.values_list('id', flat=True)),
        ]
        for magic_weapon_type in MagicWeaponType.objects.filter(
            reduce(lambda x, y: x | y, queries)
        ):
            for level in magic_weapon_type.level_range():
                Weapon.create_on_base(obj, magic_weapon_type, level)


class WeaponAdmin(admin.ModelAdmin):
    ordering = (
        '-level',
        'weapon_type__name',
    )
    readonly_fields = (
        'category',
        'groups',
        'damage',
    )
    list_display = ('__str__',)
    search_fields = ['magic_item_type__name', 'weapon_type__name', 'enhancement']
    autocomplete_fields = ('weapon_type',)
    form = WeaponForm

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    @staticmethod
    def _get_search_request_sender(request: HttpRequest):
        # ugly workaround to filter results for autocomplete field
        url_parts = urllib.parse.urlparse(request.get_full_path())
        query_parts = urllib.parse.parse_qs(url_parts.query)
        return (
            query_parts['app_label'][0],
            query_parts['model_name'][0],
            query_parts['field_name'][0],
        )

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        app_label, model_name, field_name = self._get_search_request_sender(request)
        if app_label != 'base' or model_name != 'npc':
            return queryset, may_have_duplicates
        if field_name == 'no_hand':
            queryset = queryset.filter(
                weapon_type__handedness__is_one_handed__isnull=True
            )
        return queryset, may_have_duplicates

    def get_queryset(self, request):
        return super().get_queryset(request).with_enhancement()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'magic_item_type':
            kwargs['queryset'] = MagicItemType.objects.filter(
                slot=MagicItemSlot.WEAPON.value
            ).order_by('name')
        return super(WeaponAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    @admin.display(description='Категория оружия')
    def category(self, obj):
        return str(obj.category)

    @admin.display(description='Группа оружия')
    def groups(self, obj):
        return ', '.join(
            WeaponGroupEnum(wg).description
            for wg in obj.weapon_type.groups.values_list('name', flat=True)
        )

    @admin.display(description='Урон')
    def damage(self, obj):
        return f'{obj.weapon_type.damage()} + {obj.enhancement}'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=...):
        return False

    def has_delete_permission(self, request, obj=...):
        return False


class PowerPropertyInline(admin.TabularInline):
    model = PowerProperty
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4, 'cols': 60})},
    }

    def get_extra(self, request, obj=None, **kwargs):
        querystring_extra = (
            len([key for key in request.GET.keys() if key.startswith('properties')])
            // 2
        )
        return querystring_extra or super().get_extra(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'subclass':
            object_id = request.resolver_match.kwargs.get('object_id', 0)
            try:
                instance = self.parent_model.objects.get(id=object_id)
            except self.parent_model.DoesNotExist:
                instance = None
            if instance and instance.klass:
                db_field.choices = instance.klass.subclasses.generate_choices()

        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)

        if obj:
            return FormSet

        # Собираем initial данные из GET-параметров
        initial = []
        max_index = -1

        # Находим максимальный индекс из параметров
        for key in request.GET:
            if key.startswith('properties-'):
                parts = key.split('-')
                if len(parts) == 3:
                    index = int(parts[1])
                    max_index = max(max_index, index)

        if max_index >= 0:
            initial = [{} for _ in range(max_index + 1)]
            for key, value in request.GET.items():
                if key.startswith('properties-'):
                    parts = key.split('-')
                    if len(parts) == 3:
                        index = int(parts[1])
                        field = parts[2]
                        initial[index][field] = value

        class CustomFormSet(FormSet):
            def __init__(self, *args, **kwargs):
                kwargs['initial'] = initial
                super().__init__(*args, **kwargs)

        return CustomFormSet


class PowerAdminBase(TextFromImage):
    BELONGS_TO = ''

    inlines = (PowerPropertyInline,)
    readonly_fields = ('syntax',)
    autocomplete_fields = ('weapon_types',)
    radio_fields = {
        'frequency': admin.VERTICAL,
        'action_type': admin.VERTICAL,
        'attack_ability': admin.VERTICAL,
        'defence': admin.VERTICAL,
        'accessory_type': admin.VERTICAL,
        'range_type': admin.VERTICAL,
    }
    form = PowerForm
    save_as = True

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if self.model._meta.app_label == 'base':
            return {}

        return super().get_model_perms(request)

    @admin.display(description='Синтаксис')
    def syntax(self, obj):
        return textwrap.dedent(
            '''
            str - модификатор силы
            con - модификатор телосложения
            dex - модификатор ловкости
            int - модификатор интеллекта
            wis - модификатор мудрости
            cha - модификатор харизмы
            wpn - урон от оружия (кубы + бонус зачарования)
            wps - урон от вторичного оружия (кубы + бонус зачарования)
            lvl - уровень персонажа
            dmg - бонус урона (= бонусу за уровень + бонусу урона от класса)
            dms - бонус урона вторичного оружия
            atk - бонус атаки (= бонусу за уровень + пол уровня + бонус атаки от класса)
            atk - бонус атаки вторичного оружия
            eht - зачарование оружия
            ehs - зачарование вторичного оружия
            itl - уровень предмета, к которому принадлежит талант

            Выражения начинаются со знака $.
            поддерживаются операции +, -, *, / с целыми числами, ^ (max), _ (min).
            Атака по умолчанию $[ATTACK_ATTRIBUTE]+atk+[power.attack_bonus]
            Урон по умолчанию $wpn+dmg / $[damage_dice]+dmg+[ATTACK_ATTRIBUTE]
            '''
        )

    def get_fields(self, request, obj=None):
        if not obj or obj.frequency == PowerFrequencyIntEnum.PASSIVE:
            return (
                ('upload_from_clipboard', 'from_image'),
                'name',
                'description',
                'level',
                self.BELONGS_TO,
                ('frequency', 'action_type'),
            )
        return [
            'name',
            'description',
            'level',
            self.BELONGS_TO,
            ('frequency', 'action_type'),
            ('attack_ability', 'defence', 'attack_bonus'),
            ('effects', 'damage_types'),
            ('dice_number', 'damage_dice'),
            ('accessory_type', 'weapon_types'),
            ('range_type', 'range', 'burst'),
            'syntax',
        ]

    def get_list_filter(self, request):
        return 'frequency', self.BELONGS_TO

    def get_ordering(self, request):
        return 'level', 'frequency', 'name', self.BELONGS_TO

    def get_list_display(self, request):
        return 'name', self.BELONGS_TO, 'level', 'frequency'

    def get_search_fields(self, request):
        return 'name', f'{self.BELONGS_TO}__name'

    def get_inlines(self, request, obj):
        if obj:
            return super().get_inlines(request, obj)
        return ()

    def save_model(self, request, obj, form, change):
        if getattr(form, 'show_duplicate_warning', False):
            messages.warning(request, '⚠️ Запись с таким именем уже существует!')

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        if not obj.attack_ability:
            return
        ability_mod = obj.attack_ability.short_name
        for property in obj.properties.filter(title=PowerPropertyTitle.ATTACK):
            if not property.description:
                property.description = (
                    f'${ability_mod}+atk+{obj.attack_bonus} '
                    f'против {obj.defence_subjanctive}'
                )
            elif property.description.startswith('+'):
                property.description = (
                    f'${ability_mod}+atk+{obj.attack_bonus} '
                    f'против {obj.defence_subjanctive}. {property.description[1:]}'
                )
            property.save()
        for property in obj.properties.filter(title=PowerPropertyTitle.HIT):
            if obj.level == 1 and obj.frequency == PowerFrequencyIntEnum.AT_WILL:
                # at will first level powers damage changes from 1WPN to 2WPN
                # on 21 level
                at_will_first_level_modifier = '(lvl/21+1)*'
            else:
                at_will_first_level_modifier = ''
            if obj.accessory_type == AccessoryTypeEnum.WEAPON:
                default_string = (
                    f'Урон ${at_will_first_level_modifier}'
                    f'wpn*{obj.dice_number}+dmg+{ability_mod}'
                )
            elif obj.accessory_type == AccessoryTypeEnum.IMPLEMENT:
                default_string = (
                    f'Урон ${at_will_first_level_modifier}'
                    f'{obj.dice_number}{obj.get_damage_dice_display()}'
                    f'+dmg+{ability_mod}'
                )
            else:
                continue
            if not property.description:
                property.description = default_string
            elif property.description.startswith('+'):
                property.description = default_string + property.description[1:]
            property.save()
        for property in obj.properties.filter(title=PowerPropertyTitle.TARGET):
            if not property.description:
                property.description = property.power.default_target
                property.save()
        for property in obj.properties.filter(title=PowerPropertyTitle.MISS):
            if not property.description:
                property.description = 'Половина урона'
                property.save()

    def _apply_parsed_data(self, text, obj):
        print(text)
        # TODO finish it up


class PowerAdmin(PowerAdminBase):
    BELONGS_TO = 'belongs_to'

    list_filter = (
        'frequency',
        ('klass', admin.RelatedOnlyFieldListFilter),
        ('race', admin.RelatedOnlyFieldListFilter),
        ('functional_template', admin.RelatedOnlyFieldListFilter),
        ('paragon_path', admin.RelatedOnlyFieldListFilter),
        ('magic_item_type', admin.RelatedOnlyFieldListFilter),
        ('skill', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = (
        'name',
        'klass__name_display',
        'race__name_display',
        'functional_template__title',
        'paragon_path__title',
        'magic_item_type__name',
        'skill__title',
    )

    @admin.display(description='Принадлежит')
    def belongs_to(self, obj) -> str:
        if obj.subclass:
            return obj.subclass
        if obj.klass:
            return obj.klass
        if obj.race:
            return obj.race
        if obj.functional_template:
            return obj.functional_template
        if obj.paragon_path:
            return obj.paragon_path
        if obj.magic_item_type:
            return obj.magic_item_type
        if obj.skill:
            return obj.skill
        return ''

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return 'syntax', self.BELONGS_TO

    def get_ordering(self, request):
        return 'level', 'frequency', 'name'

    def get_list_filter(self, request):
        return ('frequency',)

    def get_list_display(self, request):
        return 'name', self.BELONGS_TO, 'level', 'frequency'

    def get_search_fields(self, request):
        return ('name',)


class PowerChildAdminBase(PowerAdminBase):
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(**{f'{self.BELONGS_TO}__isnull': False})
        )

    def get_fields(self, request, obj=None):
        return [
            'name',
            'description',
            'level',
            self.BELONGS_TO,
            ('frequency', 'action_type'),
            ('attack_ability', 'defence', 'attack_bonus'),
            ('effects', 'damage_types'),
            ('dice_number', 'damage_dice'),
            ('accessory_type', 'weapon_types'),
            ('range_type', 'range', 'burst'),
            'syntax',
        ]

    def get_inlines(self, request, obj):
        return self.inlines


class ClassPowerAdmin(PowerChildAdminBase):
    BELONGS_TO = 'klass'

    def get_search_fields(self, request):
        return 'name', f'{self.BELONGS_TO}__name_display'


class SubclassPowerAdmin(PowerChildAdminBase):
    BELONGS_TO = 'subclass'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(subclass__subclass_id__gt=0)


class RacePowerAdmin(PowerChildAdminBase):
    BELONGS_TO = 'race'

    def get_search_fields(self, request):
        return 'name', f'{self.BELONGS_TO}__name_display'


class FunctionalTemplatePowerAdmin(PowerChildAdminBase):
    BELONGS_TO = 'functional_template'

    def get_search_fields(self, request):
        return 'name', f'{self.BELONGS_TO}__title'

    def get_list_display(self, request):
        return 'name', self.BELONGS_TO, 'frequency'

    def get_ordering(self, request):
        return 'name', self.BELONGS_TO, 'frequency'


class ParagonPathPowerAdmin(PowerChildAdminBase):
    BELONGS_TO = 'paragon_path'
    form = ParagonPathPowerForm

    def get_search_fields(self, request):
        return 'name', f'{self.BELONGS_TO}__title'


class MagicItemTypePowerAdmin(PowerChildAdminBase):
    BELONGS_TO = 'magic_item_type'

    def get_list_display(self, request):
        return 'name', self.BELONGS_TO, 'frequency'

    def get_ordering(self, request):
        return self.BELONGS_TO, 'frequency', 'name'


class SkillPowerAdmin(PowerChildAdminBase):
    BELONGS_TO = 'skill'

    def get_search_fields(self, request):
        return 'name', f'{self.BELONGS_TO}__title'


class FunctionalTemplateAdmin(admin.ModelAdmin):
    fields = (
        ('title', 'min_level'),
        ('armor_class_bonus', 'fortitude_bonus', 'reflex_bonus', 'will_bonus'),
        ('save_bonus', 'action_points_bonus', 'hit_points_per_level'),
    )
    list_display = ('title', 'min_level')
    list_editable = ('min_level',)
    inlines = (PowerReadonlyInline,)


class PlayerCharactersAdmin(admin.ModelAdmin):
    fields = (
        'name',
        ('armor_class', 'fortitude', 'reflex', 'will'),
        ('passive_perception', 'passive_insight'),
        'initiative',
    )
    list_display = (
        'name',
        'armor_class',
        'fortitude',
        'reflex',
        'will',
        'passive_perception',
        'passive_insight',
        'initiative',
    )
    list_editable = list_display[1:]
    ordering = ('name',)


class MonsterAdmin(TextFromImage):
    fields = (
        ('upload_from_clipboard', 'from_image'),
        ('name', 'role', 'level', 'size'),
        ('armor_class', 'fortitude', 'reflex', 'will'),
        (
            'hit_points',
            'speed',
            'initiative',
        ),
        'avatar',
        'source',
    )
    list_display = ('name', 'role', 'level')
    form = MonsterForm

    def _apply_parsed_data(self, text, obj):
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Имя и Тип
        if lines:
            types = r"(Миньон|Артиллерия|Громила|Контроллер|Налётчик|Соглядатай|Солдат)"
            name_type_match = re.match(rf"(.+?)\s+{types}\s+(\d+) уровня", lines[0])
            if name_type_match:
                obj.name = name_type_match.group(1).strip()
                obj.role = name_type_match.group(2)
                obj.level = int(name_type_match.group(3))

        size_pattern = r"(Крошечный|Средний|Маленький|Большой|Огромный|Гигантский)"
        for line in lines:
            if re.search(size_pattern, line):
                obj.size = SizeIntEnum.get_by_description(
                    re.search(size_pattern, line).group(1)
                )
                break

        # Инициатива и Внимательность
        for line in lines:
            initiative_match = re.search(r"Инициатива\s*([+-]\d+)", line)
            # perception_match = re.search(r"Внимательность\s*([+-]\d+)", line)
            hit_points_match = re.search(r'Хиты\s*(\d+)', line)

            if initiative_match:
                obj.initiative = int(initiative_match.group(1))
            # if perception_match:
            #     form.cleaned_data["Внимательность"] = int(perception_match.group(1))
            if hit_points_match:
                obj.hit_points = int(hit_points_match.group(1))

        # Защиты
        defenses = {
            'armor_class': r"КД\s*(\d+)",
            'fortitude': r"Стойкость\s*(\d+)",
            'reflex': r"Реакция\s*(\d+)",
            'will': r"Воля\s*(\d+)",
        }

        for key, pattern in defenses.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                setattr(obj, key, int(match.group(1)))

        hp_match = re.search(r"Хиты\s*(\d+)", text)
        if hp_match:
            obj.hip_points = int(hp_match.group(1))

        speed_match = re.search(r"Скорость\s*(\d+)", text)
        if speed_match:
            obj.speed = int(speed_match.group(1))

        # abilities_pattern = r"(Сил|Лов|Мдр|Тел|Инт|Хар)\s+(\d+)"
        # matches = re.findall(abilities_pattern, text)
        #
        # for ability, value in matches:
        #     setattr(obj, ability, int(value))


class MagicItemTypeAdminBase(admin.ModelAdmin):
    ordering = ('name',)
    readonly_fields = ('image_tag',)
    inlines = (PowerReadonlyInline, BonusInline)

    @admin.display(description='Картинка')
    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.picture.url}" />')

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['upload_from_clipboard']:
            bashCommand = 'xclip -selection clipboard -t image/png -o'
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            image_field = ImageFile(io.BytesIO(output), name=f'MagicItem_{obj.id}.png')
            obj.picture = image_field
        super().save_model(request, obj, form, change)


class MagicItemTypeAdmin(MagicItemTypeAdminBase):
    fields = (
        'name',
        'slot',
        ('min_level', 'step', 'max_level'),
        'category',
        'picture',
        'upload_from_clipboard',
        'image_tag',
        'book_source',
    )
    autocomplete_fields = ('book_source',)

    form = MagicItemTypeForm
    list_display = ('name', 'slot')

    @atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not MagicItemSlot(obj.slot).is_simple():
            return

        for level in obj.level_range():
            if not SimpleMagicItem.objects.filter(
                magic_item_type=obj, level=level
            ).exists():
                magic_item = SimpleMagicItem(magic_item_type=obj, level=level)
                magic_item.save()


class MagicArmorTypeAdmin(MagicItemTypeAdminBase):
    fields = (
        'name',
        'armor_type_slots',
        ('min_level', 'step', 'max_level'),
        'category',
        'picture',
        'upload_from_clipboard',
        'image_tag',
        'book_source',
    )
    autocomplete_fields = ('book_source',)
    form = MagicArmorTypeForm
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    @atomic
    def save_model(self, request, obj, form, change):
        obj.slot = MagicItemSlot.ARMOR.value
        super().save_model(request, obj, form, change)
        if change:
            return
        armor_types = ArmorType.objects.filter(
            base_armor_type__id__in=obj.armor_type_slots.values_list('id', flat=True)
        )
        for armor_type in armor_types:
            for level in obj.level_range():
                Armor.create_on_base(armor_type, obj, level)


class MagicWeaponTypeAdmin(MagicItemTypeAdminBase):
    fields = (
        'name',
        (
            'weapon_categories',
            'weapon_groups',
        ),
        'weapon_types',
        'implement_type',
        ('min_level', 'step', 'max_level'),
        'category',
        ('crit_dice', 'crit_property'),
        'picture',
        'upload_from_clipboard',
        'image_tag',
        'book_source',
    )
    autocomplete_fields = ('book_source',)
    form = MagicWeaponTypeForm

    @atomic
    def save_model(self, request, obj, form, change):
        obj.slot = MagicItemSlot.WEAPON.value
        super().save_model(request, obj, form, change)
        queries = [
            models.Q(id__in=obj.weapon_types.values_list('id', flat=True)),
            models.Q(category__in=obj.weapon_categories.all()),
            models.Q(groups__in=obj.weapon_groups.all()),
        ]
        weapon_types = (
            WeaponType.objects.prefetch_related('groups')
            .filter(reduce(lambda x, y: x | y, queries))
            .filter(is_enhanceable=True)
        )
        for weapon_type in weapon_types:
            for level in obj.level_range():
                Weapon.create_on_base(weapon_type, obj, level)
        # deleting weapons that can no longer be of unchecked weapon types
        Weapon.objects.filter(magic_item_type=obj).exclude(
            weapon_type__in=weapon_types
        ).delete()


class MagicArmItemTypeAdmin(MagicItemTypeAdminBase):
    fields = (
        'name',
        'shield_slots',
        ('min_level', 'step', 'max_level'),
        'category',
        'picture',
        'upload_from_clipboard',
        'image_tag',
        'book_source',
    )
    autocomplete_fields = ('book_source',)
    form = MagicArmItemTypeForm
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    @atomic
    def save_model(self, request, obj, form, change):
        obj.slot = MagicItemSlot.ARMS.value
        super().save_model(request, obj, form, change)
        slots = obj.shield_slots.all()
        if not slots:
            return
        for level in obj.level_range():
            for slot in slots:
                shield_type = ShieldType.objects.get(base_shield_type=slot)
                if not ArmsSlotItem.objects.filter(
                    magic_item_type=obj, shield_type=shield_type, level=level
                ).exists():
                    magic_item = ArmsSlotItem(
                        magic_item_type=obj, shield_type=shield_type, level=level
                    )
                    magic_item.save()


class MagicItemAdmin(admin.ModelAdmin):
    form = MagicItemForm
    ordering = ('magic_item_type__name', '-level')

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class ArmsItemSlotAdmin(admin.ModelAdmin):
    form = ArmsSlotItemForm

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class BonusAdmin(admin.ModelAdmin):
    autocomplete_fields = ('power',)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class BookAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class BookSourceAdmin(admin.ModelAdmin):
    search_fields = ('book__name', 'page_number')

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class ConditionInline(admin.TabularInline):
    model = Condition
    fields = ('content_type', 'object_id')
    extra = 0
    form = ConditionForm
    show_change_link = True


class PropertiesConditionInline(admin.TabularInline):
    model = PropertiesCondition
    form = PropertiesConditionForm


class AvailabilityConditionInline(admin.TabularInline):
    model = AvailabilityCondition
    extra = 0


class ConstraintAdmin(admin.ModelAdmin):
    form = ConstraintForm
    inlines = (ConditionInline, PropertiesConditionInline, AvailabilityConditionInline)
    list_filter = ('content_type',)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    @atomic
    def save_model(self, request, obj, form, change):
        if not obj.name:
            ct = str(obj.content_type).split('|')[1].strip()
            obj.name = f'{ct}, {obj.belongs_to}, constraint'
        super().save_model(request, obj, form, change)


class ItemStateInline(admin.StackedInline):
    model = ItemState
    show_change_link = True
    extra = 0
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class FeatAdmin(admin.ModelAdmin):
    inlines = (ConstraintInline, BonusInline, ItemStateInline)
    list_display = ('name', 'min_level', 'text')
    list_editable = ('min_level',)
    search_fields = ('name', 'min_level', 'text')
    ordering = ('min_level', 'name')
    save_on_top = True
    form = FeatForm
    fields = (
        ('name', 'min_level'),
        'text',
        'race',
        ('klass', 'subclass', 'power_source'),
        'trained_skills',
        ('weapon_categories', 'weapon_types'),
        ('armor_types', 'shields'),
        ('strength', 'constitution', 'dexterity'),
        ('intelligence', 'wisdom', 'charisma'),
    )

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if self.model._meta.app_label == 'base':
            return {}

        return super().get_model_perms(request)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if any(
            (
                form.cleaned_data.get('klass'),
                form.cleaned_data.get('subclass'),
                form.cleaned_data.get('power_source'),
                form.cleaned_data.get('race'),
                form.cleaned_data.get('trained_skills'),
                form.cleaned_data.get('weapon_categories'),
                form.cleaned_data.get('weapon_types'),
                form.cleaned_data.get('armor_types'),
                form.cleaned_data.get('shields'),
                form.cleaned_data.get('strength'),
                form.cleaned_data.get('constitution'),
                form.cleaned_data.get('dexterity'),
                form.cleaned_data.get('intelligence'),
                form.cleaned_data.get('wisdom'),
                form.cleaned_data.get('charisma'),
            )
        ):
            constraint = Constraint(belongs_to=obj, name=f'Черта: {obj.name}')
            constraint.save()
            for field in ('klass', 'subclass', 'race'):
                if condition_value := form.cleaned_data.get(field):
                    condition = Condition(
                        constraint=constraint, condition=condition_value
                    )
                    condition.save()
            if skills := form.cleaned_data.get('trained_skills'):
                for skill in skills:
                    condition = Condition(constraint=constraint, condition=skill)
                    condition.save()
            if any(
                (
                    form.cleaned_data.get('weapon_categories'),
                    form.cleaned_data.get('weapon_types'),
                    form.cleaned_data.get('armor_types'),
                    form.cleaned_data.get('shields'),
                )
            ):
                condition = AvailabilityCondition(
                    armor_types=form.cleaned_data.get('armor_types'),
                    shields=form.cleaned_data.get('shields'),
                    constraint=constraint,
                )
                condition.save()
                condition.weapon_categories.set(
                    form.cleaned_data.get('weapon_categories')
                )
                condition.weapon_types.set(form.cleaned_data.get('weapon_types'))

            for field in (
                'strength',
                'constitution',
                'dexterity',
                'intelligence',
                'wisdom',
                'charisma',
                'power_source',
            ):
                if condition_value := form.cleaned_data.get(field):
                    condition = PropertiesCondition(
                        constraint=constraint, type=field.upper(), value=condition_value
                    )
                    condition.save()


class WeaponStateAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
