from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PrinterConfig(AppConfig):
    name = 'printer'
    verbose_name = _('Printer')
