from django.db import models
from django.db.transaction import atomic
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import DiceIntEnum, SizeIntEnum
from base.managers import EncounterParticipantsQuerySet
from base.models.books import BookSource
from base.models.models import NPC


class PlayerCharacter(models.Model):
    class Meta:
        verbose_name = _('Player character')
        verbose_name_plural = _('Player characters')

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

    def __str__(self) -> str:
        return self.name


class Monster(models.Model):
    name = models.CharField(
        verbose_name=_('Name'), max_length=50, null=True, blank=True
    )
    level = models.PositiveSmallIntegerField(verbose_name=_('Level'), default=1)
    role = models.CharField(verbose_name=_('Role'), default='Солдат', max_length=20)
    size = models.SmallIntegerField(
        verbose_name=_('Size'),
        choices=SizeIntEnum.generate_choices(),
        default=SizeIntEnum.MEDIUM.value,
    )
    armor_class = models.PositiveSmallIntegerField(
        verbose_name=_('Armor class'), default=10
    )
    fortitude = models.PositiveSmallIntegerField(
        verbose_name=_('Fortitude'), default=10
    )
    reflex = models.PositiveSmallIntegerField(verbose_name=_('Reflex'), default=10)
    will = models.PositiveSmallIntegerField(verbose_name=_('Will'), default=10)
    hit_points = models.PositiveSmallIntegerField(
        verbose_name=_('Hit points'), default=10
    )
    speed = models.PositiveSmallIntegerField(verbose_name=_('Speed'), default=6)
    initiative = models.SmallIntegerField(verbose_name=_('Initiative'), default=0)

    avatar = models.ForeignKey(
        'printer.Avatar',
        verbose_name=_('Avatar'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'pc__isnull': True, 'npc__isnull': True},
    )
    source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name or ''


class Party(models.Model):
    class Meta:
        verbose_name = _('Party')
        verbose_name_plural = _('Parties')

    name = models.CharField(
        verbose_name=_('Name'), default='', blank=True, max_length=20
    )
    members = models.ManyToManyField(
        PlayerCharacter, verbose_name=_('Player characters')
    )
    npc_members = models.ManyToManyField(
        NPC, verbose_name=_('Non player characters'), blank=True
    )

    def __str__(self):
        members = ', '.join(
            self.members.order_by('name').values_list('name', flat=True)
        )
        if self.npc_members.count():
            npcs = ', '.join(
                self.npc_members.order_by('name').values_list('name', flat=True)
            )
            npcs = f'; {npcs}'
        else:
            npcs = ''
        name = f'{self.name}: ' if self.name else ''
        return f'{name}{members}{npcs}'

    def get_absolute_url(self):
        return reverse('party', kwargs={'pk': self.pk})


class Encounter(models.Model):
    class Meta:
        verbose_name = _('Encounter')
        verbose_name_plural = _('Encounters')

    short_description = models.CharField(
        max_length=30, verbose_name=_('Short description'), null=True, blank=True
    )
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    roll_for_players = models.BooleanField(
        verbose_name='Кидать инициативу за игроков?', default=False
    )
    party = models.ForeignKey(
        Party,
        verbose_name=_('Party'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    npcs = models.ManyToManyField(NPC, verbose_name='Мастерские персонажи', blank=True)
    pcs = models.ManyToManyField(
        PlayerCharacter,
        verbose_name=_('Player characters'),
        blank=True,
        through='base.CombatantPC',
    )
    monsters = models.ManyToManyField(
        Monster, verbose_name=_('Monsters'), blank=True, through='base.CombatantMonster'
    )
    turn_number = models.PositiveSmallIntegerField(verbose_name='Номер хода', default=1)
    is_passed = models.BooleanField(verbose_name='Сцена сыграна', default=False)

    def __str__(self) -> str:
        if self.short_description:
            return f'Сцена {self.short_description}'
        return f'Сцена №{self.id}'

    def next_turn(self, form) -> None:
        while True:
            self.turn_number += 1
            if self.participants.ordered()[self.turn_number_in_round - 1].is_active:
                break
        EncounterParticipants.save_statuses(self, form)
        self.save()

    def previous_turn(self, form) -> None:
        while True:
            self.turn_number -= 1
            if self.participants.ordered()[self.turn_number_in_round - 1].is_active:
                break
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
        if self.party:
            for pc in self.party.members.all():
                if self.combatants_pcs.filter(pc=pc).count():
                    continue
                cpc = CombatantPC(pc=pc, encounter=self)
                cpc.save()
                self.combatants_pcs.add(cpc)
            self.npcs.add(*self.party.npc_members.all())
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
                    name=f"{npc.name}, {npc.klass}",
                    initiative=npc.initiative + DiceIntEnum.D20.roll(),
                    ac=npc.armor_class,
                    fortitude=npc.fortitude,
                    reflex=npc.reflex,
                    will=npc.will,
                    number=0,
                )
            )
        for combatant in self.combatants_monsters.all():
            initiative = combatant.monster.initiative + DiceIntEnum.D20.roll()
            for i in range(combatant.number):
                participants.append(
                    EncounterParticipants(
                        encounter=self,
                        name=combatant.monster.name,
                        initiative=initiative,
                        ac=combatant.monster.armor_class,
                        fortitude=combatant.monster.fortitude,
                        reflex=combatant.monster.reflex,
                        will=combatant.monster.will,
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
    is_active = models.BooleanField(default=True)

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


class CombatantMonster(models.Model):
    class Meta:
        verbose_name = 'Участник сцены (Монстрятник)'
        verbose_name_plural = 'Участники сцены (Монстрятник)'

    encounter = models.ForeignKey(
        Encounter,
        verbose_name='Сцена',
        on_delete=models.CASCADE,
        null=True,
        related_name='combatants_monsters',
    )
    monster = models.ForeignKey(
        Monster,
        verbose_name=_('Monster'),
        on_delete=models.CASCADE,
        related_name='combatants_monsters',
        null=True,
    )
    number = models.PositiveSmallIntegerField(
        verbose_name='Количество однотипных', default=1
    )

    def __str__(self):
        return self.monster.name


class CombatantPC(models.Model):
    class Meta:
        verbose_name = 'Участник сцены (ИП)'
        verbose_name_plural = 'Участники сцены (ИП)'

    pc = models.ForeignKey(
        PlayerCharacter, verbose_name='Игровой персонаж', on_delete=models.CASCADE
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
