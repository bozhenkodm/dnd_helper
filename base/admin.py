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


class AdminMixin:
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
        return qs.annotate(title=self.ENUM.generate_case(field=self.field_name)).order_by('title')


class RaceAdmin(AdminMixin, admin.ModelAdmin):
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
        'attack_bonus',
        'npc',
    ]
    readonly_fields = ('npc',)
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
            if obj.level >= level and attr not in result:
                result.append(attr)
        return result

    def npc(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    npc.short_description = 'Лист персонажа'


class EncounterAdmin(admin.ModelAdmin):
    pass


class ArmorAdmin(admin.ModelAdmin):
    ordering = ('name',)


admin.site.register(Race, RaceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(NPC, NPCAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Armor, ArmorAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
