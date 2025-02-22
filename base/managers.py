from django.db import models
from django.db.models.functions import Floor

from base.objects.skills import Skills


class ItemAbstractQuerySet(models.QuerySet):
    def with_enhancement(self):
        return self.annotate(
            enhancement=models.Case(
                models.When(
                    magic_item_type__isnull=False,
                    then=Floor((models.F('level') - 1) / 5) + 1,
                ),
                default=0,
            ),
        )


class EncounterParticipantsQuerySet(models.QuerySet):
    def ordered(self):
        return self.order_by('-initiative', 'name')


class SkillQuerySet(models.QuerySet):
    def obj(self, value: int) -> Skills:
        return Skills(**{s.title.lower(): value for s in self})


class SubclassQuerySet(models.QuerySet):
    def generate_choices(self):
        yield from (
            (i.subclass_id, i.name) for i in self.order_by('subclass_id', 'name')
        )
