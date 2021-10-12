from django.db import models
from django.urls import reverse

from printer.constants import PrintableObjectType


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
        return reverse('printer', kwargs={'pk': self.pk})


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
