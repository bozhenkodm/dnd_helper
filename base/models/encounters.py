from django.db import models
from django.db.transaction import atomic
from django.urls import reverse

from base.constants.constants import DiceIntEnum
from base.managers import EncounterParticipantsQuerySet
from base.models.models import NPC


class PlayerCharacters(models.Model):
    class Meta:
        verbose_name = 'Игровой персонаж'
        verbose_name_plural = 'Игровые персонажи'

    name = models.CharField(verbose_name='Имя', max_length=50)
    armor_class = models.PositiveSmallIntegerField(verbose_name='КД', null=False)
    fortitude = models.PositiveSmallIntegerField(verbose_name='Стойкость', null=False)
    reflex = models.PositiveSmallIntegerField(verbose_name='Реакция', null=False)
    will = models.PositiveSmallIntegerField(verbose_name='Воля', null=False)
    initiative = models.PositiveSmallIntegerField(verbose_name='Инициатива', default=0)
    passive_perception = models.PositiveSmallIntegerField(
        verbose_name='Пассивная внимательность', default=0
    )
    passive_insight = models.PositiveSmallIntegerField(
        verbose_name='Пассивная проницательность', default=0
    )

    def __str__(self):
        return self.name


class Encounter(models.Model):
    class Meta:
        verbose_name = 'Сцена'
        verbose_name_plural = 'Сцены'

    participants: models.QuerySet  # workaround for mypy

    short_description = models.CharField(
        max_length=30, verbose_name='Краткое описание', null=True, blank=True
    )
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    roll_for_players = models.BooleanField(
        verbose_name='Кидать инициативу за игроков?', default=False
    )
    npcs = models.ManyToManyField(NPC, verbose_name='Мастерские персонажи', blank=True)
    turn_number = models.PositiveSmallIntegerField(verbose_name='Номер хода', default=1)
    is_passed = models.BooleanField(verbose_name='Сцена сыграна', default=False)

    def __str__(self):
        if self.short_description:
            return f'Сцена {self.short_description}'
        return f'Сцена №{self.id}'

    def next_turn(self, form):
        self.turn_number += 1
        EncounterParticipants.save_statuses(self, form)
        self.save()

    def previous_turn(self, form):
        self.turn_number -= 1
        EncounterParticipants.save_statuses(self, form)
        self.save()

    @property
    def url(self):
        return reverse('encounter', kwargs={'pk': self.pk})

    @property
    def round_number(self) -> int:
        if not self.participants.count():
            return 0
        if not self.turn_number % self.participants.count():
            return self.turn_number // self.participants.count()
        return self.turn_number // self.participants.count() + 1

    @property
    def turn_number_in_round(self) -> int:
        return self.turn_number % self.participants.count() or self.participants.count()

    @atomic
    def roll_initiative(self):
        self.participants.all().delete()
        self.turn_number = 1
        participants = []
        for combatant in self.combatants_pcs.all():
            if self.roll_for_players:
                initiative = combatant.pc.initiative + DiceIntEnum.D20.roll()
            else:
                initiative = combatant.initiative

            participants.append(
                EncounterParticipants(
                    encounter=self,
                    name=combatant.pc.name,
                    initiative=initiative
                    + 0.1,  # Player characters have higher initiative than npc
                    ac=combatant.pc.armor_class,
                    fortitude=combatant.pc.fortitude,
                    reflex=combatant.pc.reflex,
                    will=combatant.pc.will,
                    number=0,
                )
            )

        for npc in self.npcs.all():
            participants.append(
                EncounterParticipants(
                    encounter=self,
                    name=npc.name,
                    initiative=npc.initiative + DiceIntEnum.D20.roll(),
                    ac=npc.armor_class,
                    fortitude=npc.fortitude,
                    reflex=npc.reflex,
                    will=npc.will,
                    number=0,
                )
            )
        for combatant in self.combatants.all():
            initiative = combatant.initiative + DiceIntEnum.D20.roll()
            for i in range(combatant.number):
                participants.append(
                    EncounterParticipants(
                        encounter=self,
                        name=combatant.name,
                        initiative=initiative,
                        ac=combatant.armor_class,
                        fortitude=combatant.fortitude,
                        reflex=combatant.reflex,
                        will=combatant.will,
                        number=i + 1 if combatant.number > 1 else None,
                    )
                )
        EncounterParticipants.objects.bulk_create(participants)
        self.save()


class EncounterParticipants(models.Model):

    objects = EncounterParticipantsQuerySet.as_manager()

    encounter = models.ForeignKey(
        Encounter, on_delete=models.CASCADE, related_name='participants'
    )
    name = models.CharField(max_length=50)
    initiative = models.FloatField()
    ac = models.PositiveSmallIntegerField()
    fortitude = models.PositiveSmallIntegerField()
    reflex = models.PositiveSmallIntegerField()
    will = models.PositiveSmallIntegerField()
    number = models.SmallIntegerField(null=True)
    status = models.TextField(default='')

    def __str__(self) -> str:
        return f'{self.name} {self.number}, +{self.initiative}'

    @property
    def display_defences(self):
        return self.ac and self.fortitude and self.reflex and self.will

    @property
    def full_name(self) -> str:
        if not self.number:
            return self.name
        return f'{self.name} №{self.number}'

    def move_after(self, other: "EncounterParticipants"):
        self.initiative = other.initiative - 0.5
        self.save()

    @classmethod
    def save_statuses(cls, encounter, form):
        for number, combatant in enumerate(
            cls.objects.filter(encounter=encounter).ordered(), start=1
        ):
            combatant.status = form.get(f'status{number}')
            combatant.save()


class Combatants(models.Model):
    class Meta:
        verbose_name = 'Участник сцены (Монстрятник)'
        verbose_name_plural = 'Участники сцены (Монстрятник)'

    name = models.CharField(verbose_name='Участник сцены', max_length=50, null=False)
    encounter = models.ForeignKey(
        Encounter,
        verbose_name='Сцена',
        on_delete=models.CASCADE,
        null=True,
        related_name='combatants',
    )
    armor_class = models.PositiveSmallIntegerField(verbose_name='КД', default=0)
    fortitude = models.PositiveSmallIntegerField(verbose_name='Стойкость', default=0)
    reflex = models.PositiveSmallIntegerField(verbose_name='Реакция', default=0)
    will = models.PositiveSmallIntegerField(verbose_name='Воля', default=0)
    initiative = models.PositiveSmallIntegerField(verbose_name='Инициатива', default=0)
    number = models.PositiveSmallIntegerField(
        verbose_name='Количество однотипных', default=1
    )

    def __str__(self):
        return self.name


class CombatantsPC(models.Model):
    class Meta:
        verbose_name = 'Участник сцены (ИП)'
        verbose_name_plural = 'Участники сцены (ИП)'

    pc = models.ForeignKey(
        PlayerCharacters, verbose_name='Игровой персонаж', on_delete=models.CASCADE
    )
    encounter = models.ForeignKey(
        Encounter,
        verbose_name='Сцена',
        on_delete=models.CASCADE,
        null=True,
        related_name='combatants_pcs',
    )
    initiative = models.FloatField(verbose_name='Инициатива', default=0)

    def __str__(self):
        return str(self.pc)
