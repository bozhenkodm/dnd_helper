from django.db import models

from base.constants.constants import PowerFrequencyEnum
from base.objects import weapon_types_tuple


class WeaponTypeQuerySet(models.QuerySet):
    def with_damage_dice(self):
        kwargs = (
            {
                'slug': item.slug,
                'then': models.Value(
                    item.damage_dice.description if item.damage_dice else None
                ),
            }
            for item in weapon_types_tuple
        )
        return self.annotate(
            damage_dice=models.Case(*(models.When(**kws) for kws in kwargs))
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
