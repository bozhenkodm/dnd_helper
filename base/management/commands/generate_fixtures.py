import json
import os

from django.core.management import BaseCommand
from django.db import models

from base.models import Class, Race
from base.models.models import WeaponType
from base.objects import classes_tuple, races_tuple, weapon_types_tuple

FIXTURE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'fixtures'
)


def get_max_pk(mdl: models.Model) -> int:
    return mdl.objects.latest('id').id  # type: ignore


def generate_race_fixtures():
    race_json = []
    max_pk = get_max_pk(Race) + 1
    for race in races_tuple:
        try:
            race_db = Race.objects.get(name=race.slug.value)
        except Race.DoesNotExist:
            pk = max_pk
            max_pk += 1
            is_sociable = True
        else:
            pk = race_db.pk
            is_sociable = race_db.is_sociable
        race_json.append(
            {
                "model": "base.race",
                "pk": pk,
                "fields": {
                    "name": race.slug.value,
                    'name_display': race.slug.description,
                    'is_sociable': is_sociable,
                    'var_ability_bonus': [
                        ability.value for ability in race.var_ability_bonus.enum_objects
                    ],
                },
            }
        )
    with open(os.path.join(FIXTURE_PATH, 'race.json'), 'w') as f:
        json.dump(
            sorted(race_json, key=lambda x: x['pk']), f, indent=4, ensure_ascii=False
        )


def generate_class_fixtures():
    class_json = []
    max_pk = get_max_pk(Class) + 1
    for klass in classes_tuple:
        try:
            pk = Class.objects.get(name=klass.slug.value).pk
        except Class.DoesNotExist:
            pk = max_pk
            max_pk += 1
        class_json.append(
            {
                "model": "base.class",
                "pk": pk,
                "fields": {
                    "name": klass.slug.value,
                    "name_display": klass.slug.description,
                    'trainable_skills': [
                        skill.value for skill in klass.trainable_skills.enum_objects
                    ],
                },
            }
        )
    with open(os.path.join(FIXTURE_PATH, 'class.json'), 'w') as f:
        json.dump(
            sorted(class_json, key=lambda x: x['pk']), f, indent=4, ensure_ascii=False
        )


def generate_weapon_types_fixtures():
    class_json = []
    max_pk = get_max_pk(WeaponType) + 1
    for weapon_type in weapon_types_tuple:
        try:
            pk = WeaponType.objects.get(slug=weapon_type.__name__).pk
        except WeaponType.DoesNotExist:
            pk = max_pk
            max_pk += 1
        class_json.append(
            {
                "model": "base.weapontype",
                "pk": pk,
                "fields": {"name": weapon_type.name, "slug": weapon_type.__name__},
            }
        )
    with open(os.path.join(FIXTURE_PATH, 'weapon_types.json'), 'w') as f:
        json.dump(
            sorted(class_json, key=lambda x: x['pk']), f, indent=4, ensure_ascii=False
        )


class Command(BaseCommand):
    help = 'Generates race, class and weapon_types fixtures from python objects'

    def handle(self, *args, **options):
        generate_race_fixtures()
        generate_class_fixtures()
        generate_weapon_types_fixtures()
