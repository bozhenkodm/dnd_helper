from django.db import models

from base.constants.constants import PowerFrequencyEnum


class PowerManager(models.Manager):
    use_for_related_fields = True

    def with_frequency_order(self):
        return self.annotate(
            frequency_order=PowerFrequencyEnum.generate_order_case(field='frequency')
        )

    def ordered_by_frequency(self):
        return self.with_frequency_order().order_by('frequency_order')
