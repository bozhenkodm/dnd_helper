from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    name = models.CharField(verbose_name=_('Name'), max_length=100)
    code = models.CharField(verbose_name=_('Code'), max_length=10, unique=True)

    def __str__(self):
        return self.name


class BookSource(models.Model):
    class Meta:
        verbose_name = _('Book source')
        verbose_name_plural = _('Book sources')
        unique_together = ('book', 'book_number', 'page_number', 'is_english')

    book = models.ForeignKey(Book, verbose_name=_('Book'), on_delete=models.CASCADE)
    book_number = models.PositiveSmallIntegerField(
        verbose_name=_('Book number'), default=1
    )
    page_number = models.PositiveSmallIntegerField(verbose_name=_('Page number'))
    is_english = models.BooleanField(verbose_name=_('Is English?'), default=False)

    def __str__(self):
        return (
            f'{self.book} {self.book_number},'
            f' {self.page_number} стр.'
            f'{self.is_english * " (англ.)"}'
        )
