from django.contrib import admin

from base.admin import FeatAdmin, PowerAdmin
from features.models import Feat, Power

admin.site.register(Power, PowerAdmin)
admin.site.register(Feat, FeatAdmin)
