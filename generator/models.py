import random

from django.db import models

from base.constants.constants import NPCRaceEnum, SexEnum
from base.models import Race
from generator.constants import taverners_races


class NPCName(models.Model):
    class Meta:
        verbose_name = 'Имя'
        verbose_name_plural = 'Имена'

    FIRST_NAME = 'first'
    LAST_NAME = 'last'
    NAMETYPE_CHOICES = (
        (FIRST_NAME, 'Имя'),
        (LAST_NAME, 'Фамилия'),
    )

    name = models.CharField(max_length=30, verbose_name='Имя', unique=True)
    name_type = models.CharField(
        max_length=10, choices=NAMETYPE_CHOICES, verbose_name='Тип'
    )
    sex = models.CharField(
        max_length=SexEnum.max_length(),
        choices=SexEnum.generate_choices(is_sorted=False),
        verbose_name='Пол',
        null=True,
        blank=True,
    )
    race = models.ManyToManyField(Race)

    def __str__(self):
        return (
            f'{self.name}; '
            f'{self.get_name_type_display()}; '
            f'{self.get_sex_display()}; '
            f'{", ".join(race.get_name_display() for race in self.race.all())}'
        )

    @classmethod
    def generate_taverner(cls, race=None) -> dict:
        if not race:
            race = random.choice(taverners_races)
        else:
            race = NPCRaceEnum[race]
        race = Race.objects.get(name=race.name)
        sex = random.choice((SexEnum.M, SexEnum.F))
        first_names = cls.objects.filter(
            sex__in=(sex.name, SexEnum.N.name), name_type=cls.FIRST_NAME, race=race
        ).values_list('name', flat=True)
        last_names = cls.objects.filter(name_type=cls.LAST_NAME, race=race).values_list(
            'name', flat=True
        )
        first_name = random.choice(first_names)
        last_name = random.choice(last_names) if last_names else ''
        return {
            'first_name': first_name,
            'last_name': last_name,
            'sex': sex.name,
            'race': race.get_name_display(),
        }

    @staticmethod
    def generate_links():
        return sorted((race for race in set(taverners_races)), key=lambda x: x.value)
