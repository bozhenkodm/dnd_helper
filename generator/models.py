import random

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import SexEnum
from base.models.models import Race


class NPCName(models.Model):
    class Meta:
        verbose_name = _('Name')
        verbose_name_plural = _('Names')

    FIRST_NAME = 'first'
    LAST_NAME = 'last'
    NAMETYPE_CHOICES = (
        (FIRST_NAME, 'Имя'),
        (LAST_NAME, 'Фамилия'),
    )

    name = models.CharField(max_length=30, verbose_name=_('Name'), unique=True)
    name_type = models.CharField(
        max_length=10, choices=NAMETYPE_CHOICES, verbose_name=_('Type')
    )
    sex = models.CharField(
        max_length=SexEnum.max_length(),
        choices=SexEnum.generate_choices(is_sorted=False),
        verbose_name=_('Sex'),
        null=True,
        blank=True,
    )
    race = models.ManyToManyField(Race, verbose_name=_('Races'))

    def __str__(self):
        return (
            f'{self.name}; '
            f'{self.get_name_type_display()}; '
            f'{self.get_sex_display()}; '
            f'{", ".join(race.get_name_display() for race in self.race.all())}'
        )

    @classmethod
    def generate_npc(cls, race=None, sex=None) -> dict:
        if not race:
            race = random.choice(Race.objects.filter(is_social=True))  # type: ignore
        else:
            race = Race.objects.get(name=race)
        try:
            sex = SexEnum[sex.upper()]
        except (KeyError, AttributeError):
            sex = random.choice((SexEnum.M, SexEnum.F))
        first_names = cls.objects.filter(
            sex__in=(sex.name, SexEnum.N), name_type=cls.FIRST_NAME, race=race
        ).values_list('name', flat=True)
        last_names = cls.objects.filter(name_type=cls.LAST_NAME, race=race).values_list(
            'name', flat=True
        )
        first_name = random.choice(tuple(first_names))
        last_name = random.choice(tuple(last_names)) if last_names else ''
        return {
            'first_name': first_name,
            'last_name': last_name,
            'sex': sex.name,
            'race': race,
        }

    @staticmethod
    def generate_links():
        races = Race.objects.filter(is_social=True)
        return sorted(
            (
                (
                    race.get_name_display(),
                    reverse('generator_npc', kwargs={'race': race.name.lower()}),
                )
                for race in races
            ),
            key=lambda x: x[0],
        )


class BannedNames(models.Model):
    class Meta:
        verbose_name = _('Banned name')
        verbose_name_plural = _('Banned names')

    name = models.CharField(
        max_length=30, verbose_name=_('Name'), unique=True, null=False
    )
