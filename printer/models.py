from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import SizeIntEnum
from base.models.encounters import PlayerCharacter
from base.models.models import NPC
from printer.constants import ColorStyle, Position, PrintableObjectType, ZoneStyle


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
        default=ColorStyle.RED.value,
        max_length=ColorStyle.max_length(),
        choices=ColorStyle.generate_choices(),
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
    is_updated = models.BooleanField(editable=False, default=False)

    def update_coords(self, row, col) -> None:
        self.row = row
        self.col = col
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
        default=ColorStyle.NONE,
        max_length=ColorStyle.max_length(),
        choices=ColorStyle.generate_choices(start_with=(ColorStyle.NONE,)),
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

    def get_participants_data(self) -> dict[int, dict[int, list[tuple]]]:
        result: dict[int, dict[int, list[tuple]]] = defaultdict(dict)
        for place in self.places.all():
            for i in range(place.participant.size):
                for j in range(place.participant.size):
                    result[place.row + i].setdefault(place.col + j, []).append(
                        (
                            place.id,
                            place.participant.name,
                            place.participant.base_image.url,
                            place.rotation,
                        )
                    )
        return result

    @property
    def grid_data(self) -> list:
        """Returns a grid structure with all cell data"""
        grid = []
        participants_data = self.get_participants_data()
        zones = self.zones.all()

        for row in range(1, self.rows + 1):
            current_row = []
            for col in range(1, self.cols + 1):
                # Get cell participants
                participant = participants_data.get(row, {}).get(col, [None])[-1]

                # Zone styles and colors
                styles = []
                border_color = None
                for zone in zones:
                    if (
                        zone.top_left_x <= col <= zone.bottom_right_x
                        and zone.top_left_y <= row <= zone.bottom_right_y
                    ):
                        styles.append(f'zone-{zone.style}')
                        if zone.color != ColorStyle.NONE:
                            border_color = zone.color

                current_row.append(
                    {
                        'row': row,
                        'col': col,
                        'participant': participant,
                        'styles': ' '.join(styles),
                        'border_color': border_color,
                    }
                )
            grid.append(current_row)
        return grid

    @staticmethod
    def update_coords(participant_place_id, row, col):
        pp = ParticipantPlace.objects.get(id=participant_place_id)
        pp.update_coords(row, col)


class Zone(models.Model):
    class Meta:
        verbose_name = _('Zone')
        verbose_name_plural = _('Zones')

    map = models.ForeignKey(
        GridMap,
        verbose_name=_('Map'),
        on_delete=models.CASCADE,
        related_name='zones',
    )
    name = models.CharField(
        verbose_name=_('Name'), max_length=20, null=True, blank=True
    )
    top_left_x = models.PositiveSmallIntegerField(verbose_name=_('Top left x'))
    top_left_y = models.PositiveSmallIntegerField(verbose_name=_('Top left y'))
    bottom_right_x = models.PositiveSmallIntegerField(verbose_name=_('Bottom right x'))
    bottom_right_y = models.PositiveSmallIntegerField(verbose_name=_('Bottom right y'))
    style = models.CharField(
        verbose_name=_('Style'),
        choices=ZoneStyle.generate_choices(is_sorted=False),
        max_length=ZoneStyle.max_length(),
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_('Color'),
        max_length=20,
        choices=ColorStyle.generate_choices(start_with=(ColorStyle.NONE,)),
        null=True,
        blank=True,
    )

    def clean(self):
        super().clean()
        if (
            self.top_left_x > self.bottom_right_x
            or self.top_left_y > self.bottom_right_y
        ):
            raise ValidationError(_('Invalid zone coordinates'))
