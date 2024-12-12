from django.db import models
from django.db.models.functions import Floor

from base.constants.constants import PowerFrequencyEnum
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


class PowerQueryset(models.QuerySet):
    def with_frequency_order(self):
        return self.annotate(
            frequency_order=PowerFrequencyEnum.generate_order_case(field='frequency')
        )

    def ordered_by_frequency(self):
        return self.with_frequency_order().order_by('frequency_order')


class EncounterParticipantsQuerySet(models.QuerySet):
    def ordered(self):
        return self.order_by('-initiative', 'name')


class SkillQuerySet(models.QuerySet):
    def obj(self, value: int) -> Skills:
        return Skills(**{s.title.lower(): value for s in self})


class WeaponTypeQuerySet(models.QuerySet):
    def of_category(self, category: int):
        return self.filter(category=category)

    def of_group(self, group: str):
        return self.filter(group=group)


class SubclassQuerySet(models.QuerySet):
    def generate_choices(self):
        yield from (
            (i.subclass_id, i.name) for i in self.order_by('subclass_id', 'name')
        )
