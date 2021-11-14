# TODO handle new dataclasses in django admin
from dataclasses import asdict
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
)
from base.models import NPC, Armor, Class, Encounter, Race
from base.models.models import (
    FunctionalTemplate,
    Implement,
    Power,
    PowerTarget,
    Weapon,
    WeaponType,
)
from base.objects import implement_types_classes, npc_klasses


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
    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(title=NPCRaceEnum.generate_case())
        return qs.order_by('title')


class ClassAdmin(AdminMixin, admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields = (
        'available_armor_types',
        'available_weapons',
        'available_implements',
    )
    save_on_top = True
    ENUM = NPCClassIntEnum

    def available_armor_types(self, obj):
        return ', '.join(
            armor_type.description
            for armor_type in npc_klasses[obj.name].available_armor_types
        )

    available_armor_types.short_description = 'Ношение брони'

    def available_weapons(self, obj):
        return ', '.join(
            [
                weapon_category.description
                for weapon_category in npc_klasses[obj.name].available_weapon_categories
            ]
            + [
                weapon_type.name
                for weapon_type in npc_klasses[obj.name].available_weapon_types
            ]
        )

    available_weapons.short_description = 'Владение оружием'

    def available_implements(self, obj):
        return ', '.join(
            armor_type.name
            for armor_type in npc_klasses[obj.name].available_implement_types
        )

    available_implements.short_description = 'Владение инструментами'


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
        'mandatory_skills',
        'trained_skills',
        'armor',
        'shield',
        'weapons',
        'implements',
        'powers',
    ]
    readonly_fields = [
        'npc_link',
        'mandatory_skills',
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
                # TODO temporary (?) solution until npc.var_bonus_attr refactored
                # getting list of choices according to var_ability_bonus in race dataclass
                choices = [
                    (key.upper(), AttributeEnum[key.upper()].value)
                    for key, value in asdict(
                        instance.race_data_instance.var_ability_bonus
                    ).items()
                    if value
                ]
            else:
                choices = ()

            kwargs['choices'] = choices
        if db_field.name == 'trained_skills':
            if object_id:
                instance = self.model.objects.get(id=object_id)
                choices = instance.klass_data_instance.trainable_skills
                choices = (
                    (key.upper(), SkillsEnum[key.upper()].value)
                    for key, value in asdict(choices).items()
                    if value
                )
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
                pass
            else:
                if subclass_enum := getattr(
                    instance.klass_data_instance, 'SubclassEnum', None
                ):
                    choices = subclass_enum.generate_choices()
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
        if obj and not getattr(obj.klass_data_instance, 'SubclassEnum', None):
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

    def mandatory_skills(self, obj):
        return ', '.join(
            SkillsEnum[key.upper()]
            for key, value in asdict(obj.klass_data_instance.mandatory_skills).items()
            if value
        )

    mandatory_skills.short_description = 'Тренированные навыки'


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
    ordering = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    save_as = True


class WeaponAdmin(admin.ModelAdmin):
    ordering = (
        'name',
        'enchantment',
    )
    readonly_fields = (
        'category',
        'group',
        'damage',
    )
    list_display = ('__str__',)
    search_fields = ('name',)
    autocomplete_fields = ('weapon_type',)

    def category(self, obj):
        return obj.weapon_type.data_instance.category.description

    category.short_description = 'Категория оружия'

    def group(self, obj):
        return obj.weapon_type.data_instance.group.value

    group.short_description = 'Группа оружия'

    def damage(self, obj):
        return f'{obj.weapon_type.data_instance.damage()} + {obj.enchantment}'

    damage.short_description = 'Урон'


class ImplementAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'slug':
            db_field.choices = sorted(
                (
                    (slug, implement_type.name)
                    for slug, implement_type in implement_types_classes.items()
                ),
                key=lambda x: x[1],
            )

        return super().formfield_for_dbfield(db_field, request, **kwargs)


class PowerAdmin(admin.ModelAdmin):
    list_filter = ('frequency', 'klass', 'race', 'functional_template')
    autocomplete_fields = ('target',)
    ordering = ('klass', 'level', 'frequency')
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
            if (
                instance
                and instance.klass
                and (
                    subclass_enum := getattr(
                        npc_klasses[instance.klass.name], 'SubclassEnum', None
                    )
                )
            ):
                choices = subclass_enum.generate_choices()
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
admin.site.register(Implement, ImplementAdmin)
admin.site.register(Power, PowerAdmin)
admin.site.register(PowerTarget, PowerTargetAdmin)
admin.site.register(FunctionalTemplate, FunctionalTemplateAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
