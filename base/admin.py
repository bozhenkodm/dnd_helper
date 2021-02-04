from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe

from base.constants import (
    AttributesEnum,
    BaseCapitalizedEnum,
    NPCClassEnum,
    NPCRaceEnum,
    SkillsEnum,
    WeaponPropertyEnum,
)
from base.models import NPC, Armor, Class, Encounter, Race
from base.models.models import (
    ClassBonus,
    Implement,
    ImplementType,
    Power,
    RaceBonus,
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
        return qs.annotate(
            title=self.ENUM.generate_case(field=self.field_name)
        ).order_by('title')


class RaceBonusInline(admin.TabularInline):
    model = RaceBonus

    def save_model(self, request, obj, form, change):
        obj.name = ' '.join(item.capitalize() for item in obj.name.split())
        return super().save_model(request, obj, form, change)


class RaceAdmin(AdminMixin, admin.ModelAdmin):
    autocomplete_fields = ('available_weapon_types',)
    inlines = (RaceBonusInline,)
    ENUM = NPCRaceEnum


class ClassBonusInline(admin.TabularInline):
    model = ClassBonus

    def save_model(self, request, obj, form, change):
        obj.name = ' '.join(item.capitalize() for item in obj.name.split())
        return super().save_model(request, obj, form, change)


class ClassAdmin(AdminMixin, admin.ModelAdmin):
    inlines = (ClassBonusInline,)
    autocomplete_fields = ('available_weapon_types',)
    search_fields = ('name',)
    save_on_top = True
    ENUM = NPCClassEnum


class NPCAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'description',
        'race',
        'klass',
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
        'npc_link',
        'weapons',
        'implements',
        'powers',
    ]
    readonly_fields = ('npc_link',)
    autocomplete_fields = ('weapons', 'implements')
    list_filter = ('race', 'klass')
    save_as = True

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        object_id = request.resolver_match.kwargs.get('object_id')
        if db_field.name == 'var_bonus_attr':
            if object_id:
                instance = self.model.objects.get(id=object_id)
                choices = list(instance.race.var_bonus_attrs)
                choices = ((item, AttributesEnum[item].value) for item in choices)
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
            kwargs["queryset"] = Race.objects.annotate(
                title=NPCRaceEnum.generate_case()
            ).order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        object_id = request.resolver_match.kwargs.get('object_id', 0)
        try:
            instance = self.model.objects.get(id=object_id)
        except self.model.DoesNotExist:
            instance = None
        if db_field.name == 'powers':
            kwargs['queryset'] = Power.objects.filter(classes=instance.klass)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        if not obj:
            return (
                'name',
                'description',
                'race',
                'klass',
                'sex',
                'level',
                'base_strength',
                'base_constitution',
                'base_dexterity',
                'base_intelligence',
                'base_wisdom',
                'base_charisma',
            )
        result = super().get_fields(request, obj=obj)
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

    def npc_link(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    npc_link.short_description = 'Лист персонажа'


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
    list_filter = (
        'frequency',
        'klass',
    )
    autocomplete_fields = ('classes',)
    save_as = True


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

admin.site.unregister(Group)
admin.site.unregister(User)
