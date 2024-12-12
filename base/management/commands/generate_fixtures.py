import json
import os

from django.core.management import BaseCommand
from django.db import models

from base.models.klass import Class
from base.objects import classes_tuple

FIXTURE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'fixtures'
)


def get_max_pk(mdl: models.Model) -> int:
    return mdl.objects.latest('id').id  # type: ignore


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


class Command(BaseCommand):
    help = 'Generates race, class and weapon_types fixtures from python objects'

    def handle(self, *args, **options):
        generate_class_fixtures()
