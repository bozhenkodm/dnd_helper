from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import SizeIntEnum
from base.models.encounters import PlayerCharacter
from base.models.models import NPC
from printer.constants import ColorStyle, PrintableObjectType


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
    opacity = models.FloatField(
        verbose_name=_('Opacity'),
        default=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        choices=((0, 0), (1.0, 1.0), (0.5, 0.5)),
    )
    displayed_number = models.PositiveSmallIntegerField(
        default=0, verbose_name=_('Number')
    )
    number_in_cell = models.PositiveSmallIntegerField(default=1, editable=False)
    is_updated = models.BooleanField(editable=False, default=False)

    def update_coords(self, row: int, col: int, participants_number: int) -> None:
        self.row = row
        self.col = col
        self.number_in_cell = participants_number + 1
        self.is_updated = True
        self.save()


class Avatar(models.Model):
    class Meta:
        verbose_name = _('Avatar')
        verbose_name_plural = _('Avatars')

    MIN_SIZE = SizeIntEnum.MEDIUM

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
        default=SizeIntEnum.MEDIUM.value,
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

    @property
    def admin_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )


class MapZone(models.Model):
    class Meta:
        verbose_name = _('Zone')
        verbose_name_plural = _('Zones')

    map = models.ForeignKey(
        'printer.GridMap',
        verbose_name=_('Map'),
        on_delete=models.CASCADE,
        related_name='map_zones',
    )
    zone = models.ForeignKey(
        'printer.Zone',
        verbose_name=_('Zone type'),
        on_delete=models.CASCADE,
        related_name='map_zones',
    )
    top_left_x = models.PositiveSmallIntegerField(verbose_name=_('Top left x'))
    top_left_y = models.PositiveSmallIntegerField(verbose_name=_('Top left y'))
    custom_length = models.PositiveSmallIntegerField(
        verbose_name=_('Length'), null=True, blank=True
    )
    custom_width = models.PositiveSmallIntegerField(
        verbose_name=_('Width'), null=True, blank=True
    )
    custom_opacity = models.FloatField(
        verbose_name=_('Opacity'),
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True,
    )

    @property
    def length(self):
        return self.custom_length or self.zone.default_length

    @property
    def width(self):
        return self.custom_width or self.zone.default1_width

    @property
    def opacity(self):
        if self.custom_opacity is not None:
            return self.custom_opacity
        return self.zone.default_opacity


class Zone(models.Model):
    class Meta:
        verbose_name = _('Zone')
        verbose_name_plural = _('Zones')

    name = models.CharField(
        verbose_name=_('Name'), max_length=30, blank=True, null=True
    )
    image = models.ImageField(
        verbose_name=_('Base image'),
        upload_to='zone_types',
        null=True,
        blank=True,
    )
    default_length = models.PositiveSmallIntegerField(
        verbose_name=_('Length'), default=3
    )
    default_width = models.PositiveSmallIntegerField(verbose_name=_('Width'), default=3)
    default_opacity = models.FloatField(
        verbose_name=_('Opacity'),
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        choices=((0, 0), (0.5, 0.5), (1, 1)),
    )

    def __str__(self):
        return self.name or f'Зона {self.id}'


class GridMap(models.Model):
    class Meta:
        verbose_name = _('Map')
        verbose_name_plural = _('Maps')

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
    cells_on_longest_side = models.PositiveSmallIntegerField(
        verbose_name=_('Cells on longest side'), default=10
    )
    grid_color = models.CharField(
        verbose_name=_('Grid color'),
        default=ColorStyle.NONE.value,
        max_length=ColorStyle.max_length(),
        choices=ColorStyle.generate_choices(start_with=(ColorStyle.NONE,)),
    )
    participants = models.ManyToManyField(
        Avatar,
        through=ParticipantPlace,
        blank=True,
        verbose_name=_('Participants'),
    )
    zones = models.ManyToManyField(Zone, through=MapZone, verbose_name=_('Zones'))

    def __str__(self) -> str:
        return f'{self.name} №{self.pk}'

    @property
    def aspect_ratio(self) -> float:
        # aspect_ratio >= 1 - Landscape or square
        # aspect_ratio < 1 - Portrait
        return self.width / self.height

    @property
    def cols(self) -> int:
        if self.aspect_ratio >= 1:
            return self.cells_on_longest_side
        return round(self.cells_on_longest_side * self.aspect_ratio)

    @property
    def rows(self) -> int:
        if self.aspect_ratio >= 1:
            return round(self.cells_on_longest_side / self.aspect_ratio)
        return self.cells_on_longest_side

    @property
    def cell_size(self) -> int:
        return round(min(self.width / self.cols, self.height / self.rows))

    @property
    def url(self) -> str:
        return reverse('gridmap', kwargs={'pk': self.pk})

    @property
    def edit_url(self) -> str:
        return reverse('gridmap_edit', kwargs={'pk': self.pk})

    def get_absolute_url(self) -> str:
        return self.url

    def get_participants_data(self) -> dict[int, dict[int, list[tuple]]]:
        result: dict[int, dict[int, list[tuple]]] = defaultdict(dict)
        for place in self.places.order_by('number_in_cell'):
            for i in range(place.participant.size):
                for j in range(place.participant.size):
                    result[place.row + i].setdefault(place.col + j, []).append(
                        (
                            place.id,
                            place.participant.name,
                            place.participant.base_image.url,
                            place.rotation,
                            str(place.opacity),
                            place.displayed_number,
                        )
                    )
        return result

    @property
    def grid_data(self) -> list:
        """Returns a grid structure with all cell data"""
        grid = []
        participants_data = self.get_participants_data()

        for row in range(1, self.rows + 1):
            current_row = []
            for col in range(1, self.cols + 1):
                # Get cell participants
                participant = participants_data.get(row, {}).get(col, [None])[-1]

                zone_image_url = None
                opacity = 0
                for map_zone in self.map_zones.all():
                    if (
                        map_zone.top_left_y
                        <= row
                        < map_zone.top_left_y + map_zone.length
                        and map_zone.top_left_x
                        <= col
                        < map_zone.top_left_x + map_zone.width
                    ):
                        zone_image_url = map_zone.zone.image.url
                        opacity = map_zone.opacity
                current_row.append(
                    {
                        'row': row,
                        'col': col,
                        'participant': participant,
                        'zone': (
                            {'image_url': zone_image_url, 'opacity': str(opacity)}
                            if zone_image_url
                            else None
                        ),
                    }
                )
            grid.append(current_row)
        return grid

    def move_participant(self, participant_place_id, row, col) -> int:
        pp = ParticipantPlace.objects.get(id=participant_place_id)
        old_row, old_col = pp.row, pp.col
        participants_number_on_new_cell = ParticipantPlace.objects.filter(
            map=self, row=row, col=col
        ).count()
        pp.update_coords(row, col, participants_number_on_new_cell)
        return ParticipantPlace.objects.filter(
            map=self, row=old_row, col=old_col
        ).count()
