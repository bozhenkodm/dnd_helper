from random import randint

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe

from base.constants.base import BaseCapitalizedEnum
from base.constants.constants import (
    AttributeEnum,
    NPCClassIntEnum,
    NPCRaceEnum,
    PowerFrequencyEnum,
    SkillsEnum,
    WeaponPropertyEnum,
)
from base.constants.subclass import SUBCLASSES
from base.models import NPC, Armor, Class, Encounter, Race
from base.models.models import (
    FunctionalTemplate,
    Implement,
    ImplementType,
    Power,
    PowerTarget,
    Weapon,
    WeaponType,
)


class AdminMixin:
    enable_nav_sidebar = False

    ENUM = BaseCapitalizedEnum
    field_name = 'name'

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        object_id = request.resolver_match.kwargs.get('object_id')
        if not object_id and db_field.name == self.field_name:
            existing_races = self.model.objects.values_list(self.field_name, flat=True)
            choices = self.ENUM.generate_choices()
            kwargs['choices'] = (
                item for item in choices if item[0] not in existing_races
            )
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by(self.field_name)


class RaceAdmin(admin.ModelAdmin):
    autocomplete_fields = ('available_weapon_types',)

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(title=NPCRaceEnum.generate_case())
        return qs.order_by('title')


class ClassAdmin(AdminMixin, admin.ModelAdmin):
    autocomplete_fields = ('available_weapon_types',)
    search_fields = ('name',)
    save_on_top = True
    ENUM = NPCClassIntEnum


class NPCAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'npc_link',
        'description',
        'race',
        'klass',
        'subclass',
        'functional_template',
        'sex',
        'level',
        'base_strength',
        'base_constitution',
        'base_dexterity',
        'base_intelligence',
        'base_wisdom',
        'base_charisma',
        'var_bonus_attr',
        'trained_skills',
        'armor',
        'shield',
        'weapons',
        'implements',
        'powers',
    ]
    readonly_fields = [
        'npc_link',
        'generated_attributes',
    ]
    autocomplete_fields = ('weapons', 'implements')
    list_filter = ('race', 'klass')
    save_as = True

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        object_id = request.resolver_match.kwargs.get('object_id')
        if db_field.name == 'var_bonus_attr':
            if object_id:
                instance = self.model.objects.get(id=object_id)
                choices = list(instance.race.var_bonus_attrs)
                choices = ((item, AttributeEnum[item].value) for item in choices)
            else:
                choices = ()

            kwargs['choices'] = choices
        if db_field.name == 'trained_skills':
            if object_id:
                instance = self.model.objects.get(id=object_id)
                choices = list(instance.klass.trained_skills)
                choices = ((item, SkillsEnum[item].value) for item in choices)
            else:
                choices = ()
            kwargs['choices'] = choices

        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'race':
            kwargs['queryset'] = Race.objects.annotate(
                title=NPCRaceEnum.generate_case()
            ).order_by('title')
        if db_field.name == 'klass':
            kwargs['queryset'] = Class.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        object_id = request.resolver_match.kwargs.get('object_id', 0)
        try:
            instance = self.model.objects.get(id=object_id)
        except self.model.DoesNotExist:
            instance = None
        if db_field.name == 'powers':
            kwargs['queryset'] = Power.objects.filter(
                klass=instance.klass, level__lte=instance.level
            ).order_by('level')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'subclass':
            object_id = request.resolver_match.kwargs.get('object_id', 0)
            try:
                instance = self.model.objects.get(id=object_id)
            except self.model.DoesNotExist:
                instance = None
            subclass_enum = SUBCLASSES.get(instance.klass.name, None)
            choices = subclass_enum.generate_choices() if subclass_enum else ()
            db_field.choices = choices

        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        if not obj:
            return (
                'name',
                'description',
                'race',
                'klass',
                'sex',
                'level',
                'generated_attributes',
                'base_strength',
                'base_constitution',
                'base_dexterity',
                'base_intelligence',
                'base_wisdom',
                'base_charisma',
            )
        result = self.fields
        level_attrs_bonuses = {
            4: 'level4_bonus_attrs',
            8: 'level8_bonus_attrs',
            14: 'level14_bonus_attrs',
            18: 'level18_bonus_attrs',
            24: 'level24_bonus_attrs',
            28: 'level28_bonus_attrs',
        }
        for level, attr in level_attrs_bonuses.items():
            if obj.level >= level and attr not in result:
                result.append(attr)
        return result

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and not SUBCLASSES.get(obj.klass.name, None):
            readonly_fields.append('subclass')
        return readonly_fields

    def npc_link(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    npc_link.short_description = 'Лист персонажа'

    def generated_attributes(self, obj):
        def generate_attribute():
            l = [randint(1, 6) for _ in range(4)]
            return sum(l) - min(l)

        return ', '.join(sorted([str(generate_attribute()) for _ in range(6)], key=int))

    generated_attributes.short_description = 'Сгенерированные аттрибуты'


class EncounterAdmin(admin.ModelAdmin):
    fields = (
        'short_description',
        'description',
        'npcs',
        'encounter_link',
    )
    readonly_fields = ('encounter_link',)

    def encounter_link(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    encounter_link.short_description = 'Страница сцены'


class ArmorAdmin(admin.ModelAdmin):
    ordering = ('name',)


class WeaponTypeAdmin(admin.ModelAdmin):
    ordering = ('category', 'handedness', 'name')
    list_display = ('name', 'handedness', 'category', 'display_properties')
    list_filter = ('handedness', 'category')
    search_fields = ('name',)
    save_as = True

    def display_properties(self, obj):
        return sorted(
            item.value for item in WeaponPropertyEnum if item.name in obj.properties
        )

    display_properties.short_description = 'Свойства'


class WeaponAdmin(admin.ModelAdmin):
    ordering = (
        'weapon_type__category',
        'weapon_type__handedness',
        'name',
        'enchantment',
    )
    list_display = ('__str__', 'handedness', 'category', 'display_properties')
    list_filter = ('weapon_type__handedness', 'weapon_type__category')
    search_fields = ('name', 'weapon_type__name')
    autocomplete_fields = ('weapon_type',)

    def handedness(self, obj):
        return obj.weapon_type.get_handedness_display()

    handedness.short_description = 'Одноручное/Двуручное'

    def category(self, obj):
        return obj.weapon_type.get_category_display()

    category.short_description = 'Категория'
    category.admin_order_field = 'category'

    def display_properties(self, obj):
        return sorted(
            item.value
            for item in WeaponPropertyEnum
            if item.name in obj.weapon_type.properties
        )

    display_properties.short_description = 'Свойства'


class ImplementTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    autocomplete_fields = ('inherited_weapon_type',)

    def save_model(self, request, obj, form, change):
        obj.name = (
            form.cleaned_data['name'] or form.cleaned_data['inherited_weapon_type'].name
        )
        return super().save_model(request, obj, form, change)


class ImplementAdmin(admin.ModelAdmin):
    search_fields = ('name', 'implement_type__name')


class PowerAdmin(admin.ModelAdmin):
    list_filter = ('frequency', 'klass', 'race', 'functional_template')
    autocomplete_fields = ('target',)
    save_as = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'race':
            kwargs['queryset'] = Race.objects.annotate(
                title=NPCRaceEnum.generate_case()
            ).order_by('title')
        if db_field.name == 'klass':
            kwargs['queryset'] = Class.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        if not obj or obj.frequency == PowerFrequencyEnum.PASSIVE.name:
            return (
                'name',
                'description',
                'frequency',
                'race',
                'klass',
                'subclass',
                'functional_template',
                'level',
            )
        result = super().get_fields(request, obj)
        owner_fields = {'race', 'klass', 'functional_template'}
        for field in owner_fields:
            if getattr(obj, field):
                for obsolete_field in owner_fields - {field}:
                    result.remove(obsolete_field)
                if field != 'klass' and 'subclass' in result:
                    result.remove('subclass')
                break
        return result

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'subclass':
            object_id = request.resolver_match.kwargs.get('object_id', 0)
            try:
                instance = self.model.objects.get(id=object_id)
            except self.model.DoesNotExist:
                instance = None
            if instance.klass:
                subclass_enum = SUBCLASSES.get(instance.klass.name, None)
                choices = subclass_enum.generate_choices() if subclass_enum else ()
                db_field.choices = choices

        return super().formfield_for_dbfield(db_field, request, **kwargs)


class PowerInline(admin.StackedInline):
    exclude = ('race', 'klass', 'level', 'attack_attribute', 'defence')
    model = Power


class PowerTargetAdmin(admin.ModelAdmin):
    ordering = ('target',)
    search_fields = ('target',)


class FunctionalTemplateAdmin(admin.ModelAdmin):
    inlines = (PowerInline,)


admin.site.register(Race, RaceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(NPC, NPCAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(WeaponType, WeaponTypeAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(ImplementType, ImplementTypeAdmin)
admin.site.register(Implement, ImplementAdmin)
admin.site.register(Power, PowerAdmin)
admin.site.register(PowerTarget, PowerTargetAdmin)
admin.site.register(FunctionalTemplate, FunctionalTemplateAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
