from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GeneratorConfig(AppConfig):
    name = 'generator'
    verbose_name = _('Generator')
