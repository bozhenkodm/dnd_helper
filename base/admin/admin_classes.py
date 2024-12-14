import io
import subprocess
import textwrap
import typing
import urllib.parse
from functools import reduce

from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.files.images import ImageFile
from django.db import models
from django.db.transaction import atomic
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from base.admin.forms import (
    ArmsSlotItemForm,
    ConditionForm,
    ConstraintForm,
    MagicArmItemTypeForm,
    MagicArmorTypeForm,
    MagicItemForm,
    MagicItemTypeForm,
    MagicWeaponTypeForm,
    NPCModelForm,
    ParagonPathForm,
    WeaponForm,
)
from base.constants.constants import (
    AccessoryTypeEnum,
    ArmorTypeIntEnum,
    BonusSource,
    MagicItemSlot,
    NPCClassEnum,
    NPCRaceEnum,
    PowerFrequencyEnum,
    PowerPropertyTitle,
    PowerRangeTypeEnum,
    ShieldTypeIntEnum,
    WeaponCategoryIntEnum,
    WeaponGroupEnum,
    WeaponHandednessEnum,
)
from base.models import Race
from base.models.bonuses import Bonus
from base.models.condition import Condition, Constraint, PropertiesCondition
from base.models.encounters import Combatants, CombatantsPC
from base.models.klass import Class
from base.models.magic_items import (
    ArmsSlotItem,
    MagicArmorType,
    MagicItemType,
    MagicWeaponType,
    SimpleMagicItem,
)
from base.models.models import NPC, Armor, ArmorType, Weapon, WeaponType
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


@admin.action(description='Социализировать расы')
def make_sociable(modeladmin, request, queryset) -> None:
    queryset.update(is_sociable=True)


@admin.action(description='Десоциализировать расы')
def make_unsociable(modeladmin, request, queryset) -> None:
    queryset.update(is_sociable=False)


class RaceBonusInline(admin.TabularInline):
    model = Bonus
    fields = ('bonus_type', 'value')


class RaceAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'const_ability_bonus',
        'var_ability_bonus',
        'speed',
        'vision',
        'size',
        'weapon_types',
        'is_sociable',
    )
    list_filter = (
        'speed',
        'vision',
        'size',
        'is_sociable',
    )
    list_display = ('name_display', 'speed', 'vision', 'size', 'is_sociable')
    search_fields = ('name_display',)
    actions = (make_sociable, make_unsociable)
    inlines = (
        RaceBonusInline,
        PowerReadonlyInline,
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(title=NPCRaceEnum.generate_case())
        return qs.order_by('title')

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


class ClassBonusInline(admin.TabularInline):
    model = Bonus
    fields = ('bonus_type', 'value')


class ClassAdmin(admin.ModelAdmin):
    search_fields = ('name_display',)
    ordering = ('name_display',)
    readonly_fields = (
        'available_armor_types',
        'available_shield_types',
        'available_weapons',
        'available_implements',
        'mandatory_skills',
        'trainable_skills',
        # 'power_source',
        # 'role',
    )
    fields = readonly_fields + (
        'fortitude',
        'reflex',
        'will',
    )
    list_filter = ('power_source', 'role')
    list_display = ('name_display',)
    inlines = (ClassBonusInline,)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    # def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    @admin.display(description='Ношение брони')
    def available_armor_types(self, obj):
        return obj.armor_types

    @admin.display(description='Ношение щитов')
    def available_shield_types(self, obj):
        return obj.shields

    @admin.display(description='Владение оружием')
    def available_weapons(self, obj):
        if not obj.id:
            return '-'
        try:
            return ', '.join(
                [
                    WeaponCategoryIntEnum(int(wc)).description
                    for wc in obj.weapon_categories
                ]
                + [weapon_type.name for weapon_type in obj.weapon_types.all()]
            )
        except TypeError:
            return '-'

    @admin.display(description='Владение инструментами')
    def available_implements(self, obj):
        if not obj.id:
            return '-'
        return ', '.join(
            [implement_type.name for implement_type in obj.implement_types.all()]
        )

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
    inlines = (ClassBonusInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(subclass_id=0)

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


class RaceListFilter(admin.SimpleListFilter):
    title = 'Раса'
    parameter_name = 'race'

    def lookups(self, request, model_admin):
        return (
            Race.objects.annotate(
                name_order=NPCRaceEnum.generate_order_case(),
                verbose_name=NPCRaceEnum.generate_case(),
            )
            .values_list('name', 'verbose_name')
            .order_by('name_order')
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(race__name=self.value())


class KlassListFilter(admin.SimpleListFilter):
    title = 'Класс'
    parameter_name = 'class'

    def lookups(self, request, model_admin):
        return (
            Class.objects.annotate(
                name_order=NPCClassEnum.generate_order_case(),
            )
            .values_list('name', 'name_display')
            .order_by('name_order')
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(klass__name=self.value())


class ParagonPathAdmin(admin.ModelAdmin):
    inlines = (
        ConstraintInline,
        PowerReadonlyInline,
    )
    form = ParagonPathForm


class NPCAdmin(admin.ModelAdmin):
    # TODO fix NPC creation process
    class Meta:
        js = ('base/npc_custom.js',)

    fields = [
        (
            'name',
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
        'var_bonus_ability',
        'base_attack_ability',
        # 'level4_bonus_abilities',
        # 'level8_bonus_abilities',
        # 'level14_bonus_abilities',
        # 'level18_bonus_abilities',
        # 'level24_bonus_abilities',
        # 'level28_bonus_abilities',
        'mandatory_skills',
        'trained_skills',
        'trained_weapons',
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
        'feats',
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
        RaceListFilter,
        KlassListFilter,
        'functional_template',
        'paragon_path',
    )
    list_display = (
        'name',
        'level',
        'race',
        'klass',
        'paragon_path',
        'functional_template',
    )
    radio_fields = {"sex": admin.VERTICAL}
    list_per_page = 20
    form = NPCModelForm

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
        level_attrs_bonuses = {
            4: 'level4_bonus_abilities',
            8: 'level8_bonus_abilities',
            14: 'level14_bonus_abilities',
            18: 'level18_bonus_abilities',
            24: 'level24_bonus_abilities',
            28: 'level28_bonus_abilities',
        }
        for level, ability in level_attrs_bonuses.items():
            if obj and obj.level >= level:
                result.append(ability)
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
        result.insert(9, self._get_level_abilities_bonus_fields(obj))
        return result

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['mandatory_skills']
        if obj and obj.level < 11:
            readonly_fields.append('paragon_path')
        return readonly_fields

    @admin.display(description='Тренированные навыки')
    def mandatory_skills(self, obj):
        return ', '.join(
            s.get_title_display() for s in obj.klass.mandatory_skills.all()
        )

    @atomic
    def save_model(self, request, obj, form, change):
        # we remove all default powers on model save
        # to add it during save related
        if obj.id:
            for power in obj.powers.filter(level=0):
                obj.powers.remove(power)
        obj.experience = max(obj.experience_by_level, obj.experience)
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # we remove all default powers on model save
        # to add it during save related
        super().save_related(request, form, formsets, change)
        obj = form.instance
        default_powers = Power.objects.filter(
            models.Q(klass=obj.klass) & models.Q(subclass__in=(obj.subclass_id, 0))
        ).filter(level=0)
        for power in default_powers:
            obj.powers.add(power)


class CombatantsInlineAdmin(admin.TabularInline):
    model = Combatants

    def get_extra(self, request, obj=None, **kwargs):
        if not obj:
            return self.extra
        return 0


class CombatantsPCSInlineAdmin(admin.TabularInline):
    model = CombatantsPC

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
        CombatantsInlineAdmin,
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
        if not obj.npcs.count():
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
        for magic_armor_type in MagicArmorType.objects.filter(
            armor_type_slots__contains=obj.base_armor_type
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

    @admin.display(description='Класс доспеха')
    def armor_class(self, obj):
        if not obj.id:
            return '-'
        return obj.armor_class

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .with_enhancement()
            .annotate(
                displayed_name=ArmorTypeIntEnum.generate_value_description_case(
                    field='armor_type__base_armor_type'
                ),
            )
        )


class WeaponTypeAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'category', 'handedness')
    search_fields = ('name',)
    readonly_fields = ('prof_bonus', 'damage', 'properties')
    list_filter = ('handedness', 'category')
    save_as = True

    def get_fields(self, request, obj=None):
        if obj and obj.id:
            return (
                'category',
                'group_display',
                'prof_bonus',
                'damage',
                'handedness',
                'properties',
                'primary_end',
            )
        return (
            'slug',
            'category',
            'group',
            'prof_bonus',
            'damage',
            'handedness',
            'primary_end',
        )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    @admin.display(description='Свойства оружия')
    def properties(self, obj):
        if not obj.id:
            return '-'
        return obj.properties_text

    @admin.display(description='Группа оружия')
    def group_display(self, obj):
        if not obj.id:
            return '-'
        return ', '.join(WeaponGroupEnum[g].description for g in obj.group)

    @admin.display(description='Урон')
    def damage(self, obj):
        if not obj.id:
            return '-'
        return obj.damage()

    @atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        queries = [
            models.Q(weapon_type_slots__contains=obj.slug),
            models.Q(weapon_categories__contains=obj.slug),
        ] + [models.Q(weapon_groups__contains=g) for g in obj.group]
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
        'group',
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
                weapon_type__handedness=WeaponHandednessEnum.FREE
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
        return obj.weapon_type.category

    @admin.display(description='Группа оружия')
    def group(self, obj):
        return obj.weapon_type.group

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


class PowerAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'description',
        'level',
        ('frequency', 'action_type'),
        ('attack_ability', 'defence', 'attack_bonus'),
        ('effect_type', 'damage_type'),
        ('dice_number', 'damage_dice'),
        ('accessory_type', 'weapon_types'),
        ('range_type', 'range', 'burst'),
        'syntax',
    ]
    list_filter = (
        'frequency',
        'klass',
        RaceListFilter,
        'functional_template',
        'paragon_path',
        'magic_item_type',
        'skill',
    )
    inlines = (PowerPropertyInline,)
    readonly_fields = ('syntax',)
    ordering = ('klass', 'level', 'frequency')
    autocomplete_fields = ('weapon_types',)
    search_fields = (
        'name',
        'klass__name_display',
        'race__name_display',
        'functional_template__title',
        'paragon_path__title',
        'magic_item_type__name',
        'skill__title',
    )
    save_as = True

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'race':
            kwargs['queryset'] = Race.objects.annotate(
                title=NPCRaceEnum.generate_case()
            ).order_by('title')
        if db_field.name == 'klass':
            kwargs['queryset'] = Class.objects.order_by('name_display')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        if not obj or obj.frequency == PowerFrequencyEnum.PASSIVE:
            return (
                'name',
                'description',
                'level',
                'race',
                ('klass', 'subclass'),
                'functional_template',
                'paragon_path',
                'magic_item_type',
                'skill',
                ('frequency', 'action_type'),
            )
        result = super().get_fields(request, obj)[:]
        if obj.klass:
            result.insert(3, ('klass', 'subclass_id'))
        if obj.race:
            result.insert(3, 'race')
        if obj.functional_template:
            result.insert(3, 'functional_template')
        if obj.magic_item_type:
            result.insert(3, 'magic_item_type')
        return result

    def get_inlines(self, request, obj):
        if obj:
            return super().get_inlines(request, obj)
        return ()

    def save_related(self, request, form, formsets, change):
        super(PowerAdmin, self).save_related(request, form, formsets, change)
        obj = form.instance
        if not obj.attack_ability:
            return
        ability_mod = obj.attack_ability[:3].lower()
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
            if obj.level == 1 and obj.frequency == PowerFrequencyEnum.AT_WILL:
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
                property.description = PowerRangeTypeEnum[
                    property.power.range_type
                ].default_target()
                property.save()
        for property in obj.properties.filter(title=PowerPropertyTitle.MISS):
            if not property.description:
                property.description = 'Половина урона'
                property.save()


class FunctionalTemplateAdmin(admin.ModelAdmin):
    fields = (
        ('title', 'min_level'),
        ('armor_class_bonus', 'fortitude_bonus', 'reflex_bonus', 'will_bonus'),
        ('save_bonus', 'action_points_bonus', 'hit_points_per_level'),
    )
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
    ordering = ('name',)


class MagicItemTypeAdminBase(admin.ModelAdmin):
    ordering = ('name',)
    readonly_fields = ('image_tag',)
    inlines = (PowerReadonlyInline,)

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
        'min_level',
        'step',
        'max_level',
        'category',
        'picture',
        'upload_from_clipboard',
        'image_tag',
        'source',
    )

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
            ).count():
                magic_item = SimpleMagicItem(magic_item_type=obj, level=level)
                magic_item.save()


class MagicArmorTypeAdmin(MagicItemTypeAdminBase):
    fields = (
        'name',
        'armor_type_slots',
        'min_level',
        'step',
        'max_level',
        'category',
        'picture',
        'upload_from_clipboard',
        'image_tag',
        'source',
    )
    form = MagicArmorTypeForm

    @atomic
    def save_model(self, request, obj, form, change):
        obj.slot = MagicItemSlot.ARMOR.value
        super().save_model(request, obj, form, change)
        armor_types = ArmorType.objects.filter(
            reduce(
                lambda x, y: x | y,
                (
                    models.Q(base_armor_type__contains=slot)
                    for slot in obj.armor_type_slots
                ),
            )
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
        'min_level',
        'step',
        'max_level',
        'category',
        'crit_dice',
        'crit_property',
        'picture',
        'upload_from_clipboard',
        'image_tag',
        'source',
    )
    form = MagicWeaponTypeForm

    @atomic
    def save_model(self, request, obj, form, change):
        obj.slot = MagicItemSlot.WEAPON.value
        super().save_model(request, obj, form, change)
        queries = [
            models.Q(id__in=obj.weapon_types.values_list('id', flat=True)),
            models.Q(category__in=obj.weapon_categories),
        ] + [models.Q(group__contains=g) for g in obj.weapon_groups]
        weapon_types = WeaponType.objects.filter(
            reduce(lambda x, y: x | y, queries)
        ).filter(is_enhanceable=True)
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
        'min_level',
        'step',
        'max_level',
        'category',
        'picture',
        'upload_from_clipboard',
        'image_tag',
        'source',
    )
    form = MagicArmItemTypeForm

    @atomic
    def save_model(self, request, obj, form, change):
        obj.slot = MagicItemSlot.ARMS.value
        super().save_model(request, obj, form, change)
        slots = obj.shield_slots if obj.shield_slots else (ShieldTypeIntEnum.NONE,)
        for level in obj.level_range():
            for slot in slots:
                if not ArmsSlotItem.objects.filter(
                    magic_item_type=obj, shield=slot, level=level
                ).count():
                    magic_item = ArmsSlotItem(
                        magic_item_type=obj, shield=slot, level=level
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


class ConditionInline(admin.TabularInline):
    model = Condition
    fields = ('content_type', 'object_id')
    extra = 0
    form = ConditionForm


class PropertiesConditionInline(admin.TabularInline):
    model = PropertiesCondition


class ConstraintAdmin(admin.ModelAdmin):
    form = ConstraintForm
    inlines = (ConditionInline, PropertiesConditionInline)

    @atomic
    def save_model(self, request, obj, form, change):
        if not obj.name:
            ct = str(obj.content_type).split('|')[1].strip()
            obj.name = f'{ct}, {obj.belongs_to}, constraint'
        super().save_model(request, obj, form, change)
