from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FeaturesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'features'
    verbose_name = _('Features')
