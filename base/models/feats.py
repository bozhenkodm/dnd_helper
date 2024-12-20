from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.abstract import ConstraintAbstract


class Feat(ConstraintAbstract):
    class Meta:
        verbose_name = _('Feat')
        verbose_name_plural = _('Feats')

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    min_level = models.PositiveSmallIntegerField(
        verbose_name=_('Minimal level'), default=1, choices=((1, 1), (11, 11), (21, 21))
    )
    text = models.TextField(verbose_name=_('Text'), null=True, blank=True)

    def __str__(self):
        constraints = []
        conditions = []
        name = (
            self.name
            if self.min_level == 1
            else f'{self.name}, {self.min_level} уровень'
        )
        for constraint in self.constraints.all():
            if constraint.conditions.count():
                conditions.append(
                    ', '.join(
                        f'{condition.content_type}: {condition.condition}'
                        for condition in constraint.conditions.all()
                    )
                )
            if constraint.scalar_conditions.count():
                conditions.append(
                    ', '.join(
                        f'{condition.get_type_display()}: {condition.value}'
                        for condition in constraint.scalar_conditions.all()
                    )
                )
            constraints.append(', '.join(conditions))
        if not constraints:
            return f'{name}. {self.text}'
        return f'{name}. {_(" or ").join(constraints)}. {self.text}'
