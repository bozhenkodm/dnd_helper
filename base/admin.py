from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe

from base.constants import (
    AttributesEnum,
    BaseCapitalizedEnum,
    NPCClass,
    NPCRace,
    SkillsEnum,
)
from base.models import NPC, Armor, Class, Encounter, Race
from base.models.models import RaceBonus, Weapon, WeaponType


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
    inlines = (RaceBonusInline,)
    ENUM = NPCRace


class ClassAdmin(AdminMixin, admin.ModelAdmin):
    ENUM = NPCClass


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
        'attack_attributes',
        'attack_bonus',
        'npc_link',
    ]
    readonly_fields = ('npc_link',)
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
                title=NPCRace.generate_case()
            ).order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        result = super().get_fields(request, obj=obj)
        level_attrs_bonuses = {
            4: 'level4_bonus_attrs',
            8: 'level8_bonus_attrs',
            14: 'level14_bonus_attrs',
            18: 'level18_bonus_attrs',
            24: 'level24_bonus_attrs',
            28: 'level28_bonus_attrs',
        }
        if not obj:
            return result
        for level, attr in level_attrs_bonuses.items():
            print(level, attr, obj.level >= level)
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
    pass


class WeaponAdmin(admin.ModelAdmin):
    pass


admin.site.register(Race, RaceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(NPC, NPCAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(WeaponType, WeaponTypeAdmin)
admin.site.register(Weapon, WeaponAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
