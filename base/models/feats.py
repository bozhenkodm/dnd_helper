from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import NPCRaceEnum
from base.models.abstract import ConstraintAbstract
from base.objects.powers_output import PowerDisplay


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
                        f'{condition.get_type_display()}: {condition.value_display}'
                        for condition in constraint.scalar_conditions.all()
                    )
                )
            constraints.append(', '.join(conditions))
        if not constraints:
            return f'{name}. {self.text}'
        return f'{name}. {_(" or ").join(constraints)}. {self.text}'


class NPCFeatAbstract(models.Model):
    class Meta:
        abstract = True

    feats = models.ManyToManyField(Feat, blank=True, verbose_name=_('Feats'))
    trained_weapons = models.ManyToManyField(
        'base.WeaponType',
        blank=True,
        verbose_name=_('Trained weapon'),
        help_text=_('Weapon training in addition to training by race and class'),
    )

    @property
    def feats_count(self) -> int:
        return self.feats.count() + self.trained_weapons.count()

    @property
    def max_feats_number(self) -> int:
        result = self.half_level + self._tier + 1
        if self.race.name == NPCRaceEnum.HUMAN:
            result += 1
        return result

    def feats_calculated(self):
        not_empty_text_query = models.Q(text__isnull=False) & ~models.Q(text='')
        feats_qs = (
            self.klass.default_feats.filter(not_empty_text_query)
            | self.subclass.default_feats.filter(not_empty_text_query)
            | self.feats.filter(not_empty_text_query)
        )
        feats: list[dict] = []
        for feat in feats_qs:
            feats.append(
                PowerDisplay(
                    name=feat.name,
                    keywords='',
                    category='Черта',
                    description=self.parse_string(
                        accessory_type=None, string=feat.text
                    ),
                    frequency_order=-1,
                    frequency='',
                    properties=[],
                ).asdict()
            )
        return feats
