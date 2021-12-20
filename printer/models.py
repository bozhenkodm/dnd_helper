from django.db import models
from django.urls import reverse

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

    def __str__(self):
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

    def __str__(self):
        return self.name

    @property
    def url(self) -> str:
        return reverse('encounter_icon', kwargs={'pk': self.pk})

    @property
    def font_size(self):
        return self.width // 4
