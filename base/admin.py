from dataclasses import asdict
from random import randint

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.db import models
from django.utils.safestring import mark_safe

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import (
    AccessoryTypeEnum,
    NPCRaceEnum,
    PowerFrequencyEnum,
    PowerPropertyTitle,
    PowerRangeTypeEnum,
    SkillsEnum,
)
from base.forms import ClassForm, NPCModelForm, WeaponTypeForm
from base.models import NPC, Armor, Class, Encounter, Race
from base.models.models import (
    Combatants,
    CombatantsPC,
    FunctionalTemplate,
    PlayerCharacters,
    Power,
    PowerProperty,
    Weapon,
    WeaponType,
)
from base.objects import npc_klasses


class RaceAdmin(admin.ModelAdmin):
    fields = ('name', 'is_sociable')

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(title=NPCRaceEnum.generate_case())
        return qs.order_by('title')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.id:
            return ('name',)
        return ()


class ClassAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields = (
        'available_armor_types',
        'available_shields',
        'available_weapons',
        'available_implements',
    )
    form = ClassForm

    def has_change_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        base = super().get_readonly_fields(request, obj)
        if obj and obj.id:
            return ('name',) + base
        return base

    def available_armor_types(self, obj):
        if not obj.id:
            return '-'
        return ', '.join(
            armor_type.description
            for armor_type in npc_klasses[obj.name].available_armor_types
        )

    available_armor_types.short_description = 'Ношение брони'

    def available_shields(self, obj):
        if not obj.id or not npc_klasses[obj.name].available_shield_types:
            return '-'
        return ', '.join(
            shield.value for shield in npc_klasses[obj.name].available_shield_types
        )

    available_shields.short_description = 'Ношение щитов'

    def available_weapons(self, obj):
        if not obj.id:
            return '-'
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
        if not obj.id:
            return '-'
        return ', '.join(
            armor_type.name
            for armor_type in npc_klasses[obj.name].available_implement_types
        )

    available_implements.short_description = 'Владение инструментами'


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


class NPCAdmin(admin.ModelAdmin):
    fields = [
        (
            'name',
            'sex',
        ),
        'npc_link',
        # 'description',
        (
            'race',
            'functional_template',
        ),
        (
            'klass',
            'subclass',
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
        'var_bonus_attr',
        'mandatory_skills',
        'trained_skills',
        (
            'armor',
            'shield',
        ),
        'weapons',
        # ('primary_hand', 'secondary_hand'),
        'powers',
    ]
    readonly_fields = [
        'npc_link',
        'mandatory_skills',
        'generated_attributes',
    ]
    autocomplete_fields = ('weapons',)
    search_fields = ('name',)
    list_filter = (RaceListFilter, 'klass')
    form = NPCModelForm
    save_as = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'race':
            kwargs['queryset'] = Race.objects.annotate(
                title=NPCRaceEnum.generate_case()
            ).order_by('title')
        if db_field.name == 'klass':
            kwargs['queryset'] = Class.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
                (
                    'name',
                    'sex',
                ),
                'description',
                (
                    'race',
                    'functional_template',
                ),
                'klass',
                'level',
                'generated_attributes',
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
            generated_sum = [randint(1, 6) for _ in range(4)]
            return sum(generated_sum) - min(generated_sum)

        return ', '.join(sorted([str(generate_attribute()) for _ in range(6)], key=int))

    generated_attributes.short_description = 'Сгенерированные аттрибуты'

    def mandatory_skills(self, obj):
        return ', '.join(
            SkillsEnum[key.upper()]
            for key, value in asdict(obj.klass_data_instance.mandatory_skills).items()
            if value
        )

    mandatory_skills.short_description = 'Тренированные навыки'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for power in obj.powers.filter(level=0):
            obj.powers.remove(power)
        obj.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        default_powers = Power.objects.filter(
            models.Q(klass=obj.klass) & models.Q(subclass__in=(obj.subclass, 0))
        ).filter(level=0)
        for power in default_powers:
            obj.powers.add(power)


class CombatantsInlineAdmin(admin.TabularInline):
    model = Combatants


class CombatantsPCSInlineAdmin(admin.TabularInline):
    model = CombatantsPC


class EncounterAdmin(admin.ModelAdmin):
    fields = (
        'short_description',
        'roll_for_players',
        ('npcs', 'npc_links'),
        'encounter_link',
    )
    readonly_fields = ('encounter_link', 'npc_links')
    inlines = (
        CombatantsPCSInlineAdmin,
        CombatantsInlineAdmin,
    )
    autocomplete_fields = ('npcs',)

    def encounter_link(self, obj):
        if not obj.id:
            return '-'
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    encounter_link.short_description = 'Страница сцены'

    def npc_links(self, obj):
        if not obj.npcs.count():
            return '-'
        return mark_safe(
            '<br>'.join(
                f'<a href="{npc.url}" target="_blank">{npc}</a>'
                for npc in obj.npcs.all()
            )
        )

    npc_links.short_description = 'Страницы персонажей'


class ArmorAdmin(admin.ModelAdmin):
    ordering = ('name',)


class WeaponTypeAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = (
        'category',
        'group',
        'damage',
    )
    save_as = True
    form = WeaponTypeForm

    def get_fields(self, request, obj=None):
        if obj and obj.id:
            return (
                'category',
                'group',
                'damage',
            )
        return (
            'name',
            'slug',
            'category',
            'group',
            'damage',
        )

    def has_change_permission(self, request, obj=None):
        return False

    def category(self, obj):
        if not obj.id:
            return '-'
        return obj.data_instance.category.description

    category.short_description = 'Категория оружия'

    def group(self, obj):
        if not obj.id:
            return '-'
        return obj.data_instance.group.value

    group.short_description = 'Группа оружия'

    def damage(self, obj):
        if not obj.id:
            return '-'
        return obj.data_instance.damage()

    damage.short_description = 'Урон'


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
            if (
                instance
                and instance.klass
                and instance.subclass == 0
                and (
                    subclass_enum := getattr(
                        npc_klasses[instance.klass.name], 'SubclassEnum', None
                    )
                )
            ):
                choices = subclass_enum.generate_choices()
                db_field.choices = choices
            else:
                db_field.choices = IntDescriptionSubclassEnum.generate_choices()

        return super().formfield_for_dbfield(db_field, request, **kwargs)


class PowerAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'description',
        ('frequency', 'action_type'),
        # ('klass',    'subclass'),
        # 'race',
        # 'functional_template',
        'level',
        ('attack_attribute', 'defence', 'attack_bonus'),
        ('effect_type', 'damage_type'),
        ('dice_number', 'damage_dice'),
        ('accessory_type', 'available_weapon_types'),
        ('range_type', 'range', 'burst'),
    ]
    list_filter = ('frequency', 'klass', RaceListFilter, 'functional_template')
    inlines = (PowerPropertyInline,)
    readonly_fields = ('syntax',)
    ordering = ('klass', 'level', 'frequency')
    autocomplete_fields = ('available_weapon_types',)
    save_as = True

    def syntax(self, obj):
        return '''
str - модификатор силы
con - модификатор телосложения
dex - модификатор ловкости
int - модификатор интеллекта
wis - модификатор мудрости
cha - модификатор харизмы
wpn - урон от оружия (кубы + бонус зачарования)
lvl - уровень персонажа
dmg - бонус урона (= бонусу за уровень + бонусу урона от класса)
atk - бонус атаки (= бонусу за уровень + пол уровня + бонус атаки от класса)

Выражения начинаются со знака $.
поддерживаются операции +, -, *, / с целыми числами.
Операции выполняются по порядку написания,
игнорируя арифметический порядок действий
(лень возиться со стеками и польской записью)
Атака по умолчанию $[ATTACK_ATTRIBUTE]+atk+[power.attack_bonus]
Урон по умолчанию $wpn+dmg / $[damage_dice]+dmg
'''

    syntax.short_description = 'Синтаксис'

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
                'race',
                'klass',
                # 'subclass',
                'functional_template',
            )
        result = super().get_fields(request, obj)[:]
        if obj.klass:
            result.insert(3, ('klass', 'subclass'))
        if obj.race:
            result.insert(3, 'race')
        if obj.functional_template:
            result.insert(3, 'functional_template')
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

    def get_inlines(self, request, obj):
        if obj:
            return super().get_inlines(request, obj)
        return ()

    def save_related(self, request, form, formsets, change):
        super(PowerAdmin, self).save_related(request, form, formsets, change)
        obj = form.instance
        if not obj.attack_attribute:
            return
        ability_mod = obj.attack_attribute.lower()[:3]
        for property in obj.properties.filter(title=PowerPropertyTitle.ATTACK.name):
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
        for property in obj.properties.filter(title=PowerPropertyTitle.HIT.name):
            if obj.accessory_type == AccessoryTypeEnum.WEAPON.name:
                default_string = f'Урон $wpn*{obj.dice_number}+dmg+{ability_mod}'
            elif obj.accessory_type == AccessoryTypeEnum.IMPLEMENT.name:
                default_string = (
                    f'Урон {obj.dice_number}{obj.get_damage_dice_display()}'
                    f'+$dmg+{ability_mod}'
                )
            else:
                continue
            if not property.description:
                property.description = default_string
            elif property.description.startswith('+'):
                property.description = default_string + property.description[1:]
            property.save()
        for property in obj.properties.filter(title=PowerPropertyTitle.TARGET.name):
            if not property.description:
                property.description = PowerRangeTypeEnum[
                    property.power.range_type
                ].default_target()
                property.save()
        for property in obj.properties.filter(title=PowerPropertyTitle.MISS.name):
            if not property.description:
                property.description = 'Половина урона'
                property.save()


class FunctionalTemplateAdmin(admin.ModelAdmin):
    fields = (
        ('title', 'min_level'),
        ('armor_class_bonus', 'fortitude_bonus', 'reflex_bonus', 'will_bonus'),
        ('save_bonus', 'action_points_bonus', 'hit_points_per_level'),
    )


class PlayerCharactersAdmin(admin.ModelAdmin):
    fields = (
        'name',
        ('armor_class', 'fortitude', 'reflex', 'will'),
        ('passive_perception', 'passive_insight'),
        ('initiative'),
    )


admin.site.register(Race, RaceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(NPC, NPCAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(WeaponType, WeaponTypeAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Power, PowerAdmin)
admin.site.register(FunctionalTemplate, FunctionalTemplateAdmin)
admin.site.register(PlayerCharacters, PlayerCharactersAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
