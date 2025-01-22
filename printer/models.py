from collections import defaultdict

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import SizeIntEnum
from base.models import NPC
from base.models.encounters import PlayerCharacter
from printer.constants import ColorsStyle, Position, PrintableObjectType


class PrintableObject(models.Model):
    class Meta:
        verbose_name = _('Object')
        verbose_name_plural = _('Objects')

    name = models.CharField(max_length=40, verbose_name=_('Title'))
    type = models.CharField(
        verbose_name=_('Object type'),
        choices=PrintableObjectType.generate_choices(),
        max_length=PrintableObjectType.max_length(),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f'{self.name}'

    @property
    def url(self):
        return reverse('printable_object', kwargs={'pk': self.pk})


class PrintableObjectItems(models.Model):
    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    order = models.PositiveSmallIntegerField(verbose_name=_('Order'))
    title = models.CharField(
        max_length=15, verbose_name=_('Title'), null=True, blank=True
    )
    description = models.CharField(max_length=256, verbose_name=_('Description'))
    p_object = models.ForeignKey(
        PrintableObject,
        verbose_name=_('Object'),
        on_delete=models.CASCADE,
        related_name='items',
    )


class EncounterIcons(models.Model):
    class Meta:
        verbose_name = _('Icon')
        verbose_name_plural = _('Icons')

    name = models.CharField(verbose_name=_('Title'), max_length=30)
    base_image = models.ImageField(
        verbose_name=_('Base image'),
        upload_to='encounter_icons',
        null=True,
        blank=True,
    )
    number = models.PositiveSmallIntegerField(verbose_name='Количество однотипных')
    number_color = models.CharField(
        verbose_name=_('Number color'),
        default=ColorsStyle.RED,
        max_length=ColorsStyle.max_length(),
        choices=ColorsStyle.generate_choices(),
    )
    width = models.PositiveSmallIntegerField(verbose_name=_('Width'), default=200)
    number_position = models.CharField(
        verbose_name=_('Number position'),
        choices=Position.generate_choices(),
        max_length=Position.max_length(),
        default=Position.TOP_LEFT,
    )

    def __str__(self) -> str:
        return self.name

    @property
    def url(self) -> str:
        return reverse('encounter_icon', kwargs={'pk': self.pk})

    @property
    def font_size(self) -> int:
        return self.width // 4


class ParticipantPlace(models.Model):

    participant = models.ForeignKey(
        'printer.Avatar',
        verbose_name=_('Participant'),
        on_delete=models.CASCADE,
        related_name='places',
    )
    map = models.ForeignKey(
        'printer.GridMap',
        verbose_name=_('Map'),
        on_delete=models.CASCADE,
        related_name='places',
    )
    row = models.PositiveSmallIntegerField(default=0, verbose_name=_('Row'))
    col = models.PositiveSmallIntegerField(default=0, verbose_name=_('Column'))
    rotation = models.PositiveSmallIntegerField(
        choices=((i, i) for i in range(0, 271, 90)),
        default=0,
        verbose_name=_('Rotation'),
    )

    def update_coords(self, row, col):
        self.row = row
        self.col = col
        self.save()


class Avatar(models.Model):
    MIN_SIZE = SizeIntEnum.AVERAGE

    name = models.CharField(verbose_name=_('Name'), max_length=30, blank=True)
    base_image = models.ImageField(
        verbose_name=_('Base image'),
        upload_to='avatars',
        null=True,
        blank=True,
    )
    base_size = models.SmallIntegerField(
        verbose_name=_('Size'),
        choices=SizeIntEnum.generate_choices(),
        default=SizeIntEnum.AVERAGE.value,
    )
    pc = models.OneToOneField(
        PlayerCharacter,
        verbose_name=_('Player character'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='avatar',
        limit_choices_to={'avatar__isnull': True},
    )
    npc = models.OneToOneField(
        NPC,
        verbose_name=_('Non player character'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='avatar',
        limit_choices_to={'avatar__isnull': True},
    )

    def __str__(self):
        return self.name

    @property
    def size(self) -> int:
        return max(self.base_size, self.MIN_SIZE.value)


class GridMap(models.Model):
    name = models.CharField(verbose_name=_('Title'), max_length=30, default='Карта')
    base_image = models.ImageField(
        verbose_name=_('Base image'),
        upload_to='maps',
        height_field='height',
        width_field='width',
        null=True,
        blank=True,
    )
    height = models.PositiveSmallIntegerField(verbose_name=_('Height'), default=1)
    width = models.PositiveSmallIntegerField(verbose_name=_('Width'), default=1)
    cells_on_longest_side = models.PositiveSmallIntegerField(default=10)
    grid_color = models.CharField(
        verbose_name=_('Grid color'),
        default=ColorsStyle.NONE,
        max_length=ColorsStyle.max_length(),
        choices=ColorsStyle.generate_choices(start_with=(ColorsStyle.NONE,)),
    )
    participants = models.ManyToManyField(
        Avatar,
        through=ParticipantPlace,
        blank=True,
        verbose_name=_('Participants'),
    )

    def __str__(self):
        return f'{self.name} №{self.pk}'

    @property
    def aspect_ratio(self):
        # aspect_ratio >= 1 - Landscape or square
        # aspect_ratio < 1 - Portrait
        return self.width / self.height

    @property
    def cols(self):
        if self.aspect_ratio >= 1:
            return self.cells_on_longest_side
        return round(self.cells_on_longest_side * self.aspect_ratio)

    @property
    def rows(self):
        if self.aspect_ratio >= 1:
            return round(self.cells_on_longest_side / self.aspect_ratio)
        return self.cells_on_longest_side

    @property
    def cell_size(self):
        return round(min(self.width / self.cols, self.height / self.rows))

    @property
    def url(self) -> str:
        return reverse('gridmap', kwargs={'pk': self.pk})

    @property
    def edit_url(self) -> str:
        return reverse('gridmap_edit', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return self.url

    def col_range(self):
        return range(1, self.cols + 1)

    def row_range(self):
        return range(1, self.rows + 1)

    def get_participants_data(self) -> dict[int, dict[int, list[str]]]:
        result = defaultdict(dict)
        for place in self.places.all():
            for i in range(place.participant.size):
                for j in range(place.participant.size):
                    result[place.row + i].setdefault(place.col + j, []).append(
                        (
                            place.participant.id,
                            f'{place.participant.name[0]-place.participant.name[-1]}',
                            place.participant.base_image.url
                        )
                    )
        return result

    def update_coords(self, participant_id, row, col):
        pp = ParticipantPlace.objects.get(participant_id=participant_id, map=self)
        pp.update_coords(row, col)
