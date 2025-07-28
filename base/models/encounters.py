from django.db import models
from django.db.transaction import atomic
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import DiceIntEnum, SizeIntEnum
from base.managers import EncounterParticipantsQuerySet
from base.models.books import BookSource
from base.models.models import NPC


class PlayerCharacter(models.Model):
    """Model representing a player character in D&D encounters.

    Stores character stats needed for combat including defenses,
    initiative, and passive perception/insight values.
    """

    class Meta:
        verbose_name = _('Player character')
        verbose_name_plural = _('Player characters')

    name = models.CharField(verbose_name='Имя', max_length=50)

    # Defenses
    armor_class = models.PositiveSmallIntegerField(verbose_name='КД', null=False)
    fortitude = models.PositiveSmallIntegerField(
        verbose_name='Стойкость', null=False
    )  # Fort save
    reflex = models.PositiveSmallIntegerField(
        verbose_name='Реакция', null=False
    )  # Reflex save
    will = models.PositiveSmallIntegerField(
        verbose_name='Воля', null=False
    )  # Will save

    # Combat mechanics
    initiative = models.PositiveSmallIntegerField(
        verbose_name='Инициатива', default=0
    )  # Initiative modifier

    # Passive skills for DM reference
    passive_perception = models.PositiveSmallIntegerField(
        verbose_name='Пассивная внимательность', default=0
    )
    passive_insight = models.PositiveSmallIntegerField(
        verbose_name='Пассивная проницательность', default=0
    )

    def __str__(self) -> str:
        return self.name


class Monster(models.Model):
    """Model representing a monster or NPC enemy in encounters.

    Contains complete stat block including combat stats, defenses,
    and references to avatar images and source books.
    """

    name = models.CharField(
        verbose_name=_('Name'), max_length=50, null=True, blank=True
    )
    level = models.PositiveSmallIntegerField(verbose_name=_('Level'), default=1)
    role = models.CharField(
        verbose_name=_('Role'), default='Солдат', max_length=20
    )  # Combat role (Artillery, Controller, etc.)
    size = models.SmallIntegerField(
        verbose_name=_('Size'),
        choices=SizeIntEnum.generate_choices(),
        default=SizeIntEnum.MEDIUM.value,
    )
    # Defensive stats
    armor_class = models.PositiveSmallIntegerField(
        verbose_name=_('Armor class'), default=10
    )
    fortitude = models.PositiveSmallIntegerField(
        verbose_name=_('Fortitude'), default=10
    )
    reflex = models.PositiveSmallIntegerField(verbose_name=_('Reflex'), default=10)
    will = models.PositiveSmallIntegerField(verbose_name=_('Will'), default=10)

    # Combat stats
    hit_points = models.PositiveSmallIntegerField(
        verbose_name=_('Hit points'), default=10
    )
    speed = models.PositiveSmallIntegerField(
        verbose_name=_('Speed'), default=6
    )  # Movement speed in squares
    initiative = models.SmallIntegerField(verbose_name=_('Initiative'), default=0)

    # Optional visual and reference data
    avatar = models.ForeignKey(
        'printer.Avatar',
        verbose_name=_('Avatar'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={
            'pc__isnull': True,
            'npc__isnull': True,
        },  # Only unused avatars
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
    """Model representing a group of player characters and NPCs.

    Used to organize characters for encounters and track
    party composition including both PCs and allied NPCs.
    """

    class Meta:
        verbose_name = _('Party')
        verbose_name_plural = _('Parties')

    # Party identification
    name = models.CharField(
        verbose_name=_('Name'), default='', blank=True, max_length=20
    )

    # Party composition
    members = models.ManyToManyField(
        PlayerCharacter, verbose_name=_('Player characters')
    )
    npc_members = models.ManyToManyField(
        NPC, verbose_name=_('Non player characters'), blank=True  # Allied NPCs
    )

    def __str__(self):
        # Get PC names
        members = ', '.join(
            self.members.order_by('name').values_list('name', flat=True)
        )

        # Add NPC names if any
        if self.npc_members.count():
            npcs = ', '.join(
                self.npc_members.order_by('name').values_list('name', flat=True)
            )
            npcs = f'; {npcs}'  # Separate NPCs with semicolon
        else:
            npcs = ''

        # Format with party name if provided
        name = f'{self.name}: ' if self.name else ''
        return f'{name}{members}{npcs}'

    def get_absolute_url(self):
        """Return URL for party detail view."""
        return reverse('party', kwargs={'pk': self.pk})


class Encounter(models.Model):
    """Model representing a D&D encounter/combat scene.

    Manages combat state including participants, turn order,
    initiative rolling, and encounter progression.
    """

    class Meta:
        verbose_name = _('Encounter')
        verbose_name_plural = _('Encounters')

    # Encounter description
    short_description = models.CharField(
        max_length=30, verbose_name=_('Short description'), null=True, blank=True
    )
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)

    # Initiative settings
    roll_for_players = models.BooleanField(
        verbose_name='Кидать инициативу за игроков?',
        default=False,  # Auto-roll PC initiative
    )
    # Encounter participants
    party = models.ForeignKey(
        Party,
        verbose_name=_('Party'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  # Optional: can add party to auto-populate PCs
    )
    npcs = models.ManyToManyField(NPC, verbose_name='Мастерские персонажи', blank=True)
    pcs = models.ManyToManyField(
        PlayerCharacter,
        verbose_name=_('Player characters'),
        blank=True,
        through='base.CombatantPC',
    )
    monsters = models.ManyToManyField(
        Monster,
        verbose_name=_('Monsters'),
        blank=True,
        through='base.CombatantMonster',
    )
    # Combat state tracking
    turn_number = models.PositiveSmallIntegerField(
        verbose_name='Номер хода', default=1
    )  # Absolute turn counter
    is_passed = models.BooleanField(
        verbose_name='Сцена сыграна', default=False
    )  # Encounter completed flag

    def __str__(self) -> str:
        if self.short_description:
            return f'Сцена {self.short_description}'
        return f'Сцена №{self.id}'

    def next_turn(self, form) -> None:
        """Advance to next active participant's turn.

        Increments turn counter and skips inactive participants.
        Saves participant statuses from form before advancing.
        """
        while True:
            self.turn_number += 1
            # Find next active participant in initiative order
            if self.participants.ordered()[self.turn_number_in_round - 1].is_active:
                break
        EncounterParticipants.save_statuses(self, form)
        self.save()

    def previous_turn(self, form) -> None:
        """Go back to previous active participant's turn.

        Decrements turn counter and skips inactive participants.
        Saves participant statuses from form before going back.
        """
        while True:
            self.turn_number -= 1
            # Find previous active participant in initiative order
            if self.participants.ordered()[self.turn_number_in_round - 1].is_active:
                break
        EncounterParticipants.save_statuses(self, form)
        self.save()

    @property
    def url(self):
        return reverse('encounter', kwargs={'pk': self.pk})

    @property
    def round_number(self) -> int:
        """Calculate current combat round based on turn number.

        Returns which round of combat we're in (1-indexed).
        Each round = one turn for each participant.
        """
        if not self.participants.count():
            return 0
        # If turn number is exact multiple of participant count, we're at end of round
        if not self.turn_number % self.participants.count():
            return self.turn_number // self.participants.count()
        return self.turn_number // self.participants.count() + 1

    @property
    def turn_number_in_round(self) -> int:
        """Calculate position within current round (1-indexed).

        Returns which participant's turn it is within the current round.
        """
        return self.turn_number % self.participants.count() or self.participants.count()

    @atomic
    def roll_initiative(self):
        """Roll initiative for all encounter participants.

        Clears existing participants and creates new ones with rolled initiative.
        Handles PCs (with optional auto-roll), NPCs, and monsters.
        PCs get +0.1 initiative bonus to win ties.
        """
        # Clear previous initiative order
        self.participants.all().delete()
        self.turn_number = 1
        participants = []
        # Add party members if party is set
        if self.party:
            # Add PCs from party (skip if already added manually)
            for pc in self.party.members.all():
                if self.combatants_pcs.filter(pc=pc).count():
                    continue  # Skip if PC already added manually
                cpc = CombatantPC(pc=pc, encounter=self)
                cpc.save()
                self.combatants_pcs.add(cpc)
            # Add party's NPC allies
            self.npcs.add(*self.party.npc_members.all())
        # Process player characters
        for combatant in self.combatants_pcs.all():
            if self.roll_for_players:
                # Auto-roll initiative: PC modifier + d20
                initiative = combatant.pc.initiative + DiceIntEnum.D20.roll()
            else:
                # Use manually set initiative from combatant
                initiative = combatant.initiative

            participants.append(
                EncounterParticipants(
                    encounter=self,
                    name=combatant.pc.name,
                    initiative=initiative + 0.1,  # +0.1 so PCs win initiative ties
                    ac=combatant.pc.armor_class,
                    fortitude=combatant.pc.fortitude,
                    reflex=combatant.pc.reflex,
                    will=combatant.pc.will,
                    number=0,  # PCs don't get numbers
                )
            )

        # Process NPCs (allies/neutrals)
        for npc in self.npcs.all():
            participants.append(
                EncounterParticipants(
                    encounter=self,
                    name=f"{npc.name}, {npc.klass}",  # Include class for clarity
                    initiative=npc.initiative
                    + DiceIntEnum.D20.roll(),  # Always roll for NPCs
                    ac=npc.armor_class,
                    fortitude=npc.fortitude,
                    reflex=npc.reflex,
                    will=npc.will,
                    number=0,  # NPCs don't get numbers
                )
            )
        # Process monsters (enemies)
        for combatant in self.combatants_monsters.all():
            # Roll initiative once per monster type
            initiative = combatant.monster.initiative + DiceIntEnum.D20.roll()
            # Create one participant per monster in the group
            for i in range(combatant.number):
                participants.append(
                    EncounterParticipants(
                        encounter=self,
                        name=combatant.monster.name,
                        initiative=initiative,  # Same initiative for all monsters of this type
                        ac=combatant.monster.armor_class,
                        fortitude=combatant.monster.fortitude,
                        reflex=combatant.monster.reflex,
                        will=combatant.monster.will,
                        number=(
                            i + 1 if combatant.number > 1 else None
                        ),  # Number them if multiple
                    )
                )
        # Bulk create all participants and save encounter
        EncounterParticipants.objects.bulk_create(participants)
        self.save()


class EncounterParticipants(models.Model):
    """Model representing a participant in an encounter with initiative order.

    Stores initiative-rolled stats for each combatant (PC, NPC, or monster)
    and tracks their status, activity, and position in turn order.
    """

    objects = EncounterParticipantsQuerySet.as_manager()

    # Encounter relationship
    encounter = models.ForeignKey(
        Encounter, on_delete=models.CASCADE, related_name='participants'
    )

    name = models.CharField(max_length=50)  # Display name
    number = models.SmallIntegerField(null=True)  # For multiple monsters of same type

    # Initiative and turn order
    initiative = (
        models.FloatField()
    )  # Initiative roll result (with decimal for tie-breaking)

    # Combat stats (copied from source for quick reference)
    ac = models.PositiveSmallIntegerField()
    fortitude = models.PositiveSmallIntegerField()
    reflex = models.PositiveSmallIntegerField()
    will = models.PositiveSmallIntegerField()

    # Combat state tracking
    status = models.TextField(default='')  # Custom status effects/notes
    is_active = models.BooleanField(default=True)  # Whether participant can take turns

    def __str__(self) -> str:
        return f'{self.name} {self.number}, +{self.initiative}'

    @property
    def display_defences(self):
        """Check if participant has all defense values set.

        Returns True if all defense stats are non-zero.
        """
        return self.ac and self.fortitude and self.reflex and self.will

    @property
    def full_name(self) -> str:
        """Get display name including number if applicable.

        For multiple monsters of same type, appends number.
        """
        if not self.number:
            return self.name
        return f'{self.name} №{self.number}'

    def move_after(self, other: "EncounterParticipants"):
        """Move this participant's initiative to just after another.

        Sets initiative to 0.5 less than the target participant,
        effectively moving them later in turn order.
        """
        self.initiative = other.initiative - 0.5
        self.save()

    @classmethod
    def save_statuses(cls, encounter, form):
        """Save status updates from encounter form.

        Updates status field for each participant based on form data.
        Form fields are expected to be named 'status1', 'status2', etc.
        """
        for number, combatant in enumerate(
            cls.objects.filter(encounter=encounter).ordered(), start=1
        ):
            # Get status from form field (status1, status2, etc.)
            combatant.status = form.get(f'status{number}')
            combatant.save()


class CombatantMonster(models.Model):
    """Through model for Monster participation in Encounters.

    Allows specifying how many monsters of a given type
    participate in an encounter (e.g., 3 goblins).
    """

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

    # Monster type
    monster = models.ForeignKey(
        Monster,
        verbose_name=_('Monster'),
        on_delete=models.CASCADE,
        related_name='combatants_monsters',
        null=True,
    )

    # How many of this monster type
    number = models.PositiveSmallIntegerField(
        verbose_name='Количество однотипных', default=1
    )

    def __str__(self):
        return self.monster.name


class CombatantPC(models.Model):
    """Through model for PlayerCharacter participation in Encounters.

    Allows storing PC-specific encounter data like custom initiative
    when not using auto-roll.
    """

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
