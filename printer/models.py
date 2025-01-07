from collections import defaultdict

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import SizeIntEnum
from printer.constants import ColorsStyle, Position, PrintableObjectType


class PrintableObject(models.Model):
    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    name = models.CharField(max_length=40, verbose_name='Название')
    type = models.CharField(
        verbose_name='Тип объекта',
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
        verbose_name = 'Аттрибут'
        verbose_name_plural = 'Аттрибуты'

    order = models.PositiveSmallIntegerField(verbose_name='Порядок')
    title = models.CharField(
        max_length=15, verbose_name='Название', null=True, blank=True
    )
    description = models.CharField(max_length=256, verbose_name='Описание')
    p_object = models.ForeignKey(
        PrintableObject, on_delete=models.CASCADE, related_name='items'
    )


class EncounterIcons(models.Model):
    class Meta:
        verbose_name = 'Иконка'
        verbose_name_plural = 'Иконки'

    name = models.CharField(verbose_name='Название', max_length=30)
    base_image = models.ImageField(
        verbose_name='базовая картинка',
        upload_to='encounter_icons',
        null=True,
        blank=True,
    )
    number = models.PositiveSmallIntegerField(verbose_name='Количество однотипных')
    number_color = models.CharField(
        verbose_name='Цвет номера',
        default=ColorsStyle.RED,
        max_length=ColorsStyle.max_length(),
        choices=ColorsStyle.generate_choices(),
    )
    width = models.PositiveSmallIntegerField(verbose_name='Ширина', default=200)
    number_position = models.CharField(
        verbose_name='Класс позиции номера на картинке',
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
        'printer.Participant', on_delete=models.CASCADE, related_name='places'
    )
    map = models.ForeignKey(
        'printer.GridMap', on_delete=models.CASCADE, related_name='places'
    )
    row = models.PositiveSmallIntegerField(default=0)
    col = models.PositiveSmallIntegerField(default=0)
    rotation = models.PositiveSmallIntegerField(
        choices=((i, i) for i in range(0, 271, 90)), default=0
    )


class Participant(models.Model):
    MIN_SIZE = SizeIntEnum.AVERAGE

    name = models.CharField(verbose_name='Имя', max_length=30)
    base_image = models.ImageField(
        verbose_name='Карта',
        upload_to='participants',
        null=True,
        blank=True,
    )
    base_size = models.SmallIntegerField(
        verbose_name=_('Size'),
        choices=SizeIntEnum.generate_choices(),
        default=SizeIntEnum.AVERAGE.value,
    )

    def __str__(self):
        return self.name

    @property
    def size(self) -> int:
        return max(self.base_size, self.MIN_SIZE.value)


class GridMap(models.Model):
    name = models.CharField(verbose_name='Название', max_length=30, default='Карта')
    base_image = models.ImageField(
        verbose_name='Карта',
        upload_to='maps',
        null=True,
        blank=True,
    )
    rows = models.PositiveSmallIntegerField(verbose_name='Количество строк', default=10)
    cols = models.PositiveSmallIntegerField(
        verbose_name='Количество столбцов', default=10
    )
    grid_color = models.CharField(
        verbose_name='Цвет грида',
        default=ColorsStyle.WHITE,
        max_length=ColorsStyle.max_length(),
        choices=ColorsStyle.generate_choices(),
    )
    participants = models.ManyToManyField(
        Participant, through=ParticipantPlace, blank=True
    )

    def __str__(self):
        return f'{self.name} №{self.pk}'

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

    @property
    def min_size(self):
        return 100 // min((self.rows, self.cols)) - 1

    def get_participants_data(self) -> dict[int, dict[int, list[str]]]:
        result = defaultdict(dict)
        for place in self.places.all():
            for i in range(place.participant.size):
                for j in range(place.participant.size):
                    result[place.row + i].setdefault(place.col + j, []).append(
                        place.participant.base_image.url
                    )
        return result
