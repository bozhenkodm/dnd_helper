from django.contrib import admin

from base.admin import FeatAdmin, PowerAdmin
from base.admin.admin_classes import (
    ClassPowerAdmin,
    FunctionalTemplatePowerAdmin,
    MagicItemTypePowerAdmin,
    ParagonPathPowerAdmin,
    RacePowerAdmin,
    SkillPowerAdmin,
    SubclassPowerAdmin,
)
from features.models import (
    ClassPower,
    Feat,
    FunctionalTemplatePower,
    MagicItemTypePower,
    ParagonPathPower,
    Power,
    RacePower,
    SkillPower,
    SubclassPower,
)

admin.site.register(Power, PowerAdmin)
admin.site.register(ClassPower, ClassPowerAdmin)
admin.site.register(SubclassPower, SubclassPowerAdmin)
admin.site.register(RacePower, RacePowerAdmin)
admin.site.register(FunctionalTemplatePower, FunctionalTemplatePowerAdmin)
admin.site.register(ParagonPathPower, ParagonPathPowerAdmin)
admin.site.register(MagicItemTypePower, MagicItemTypePowerAdmin)
admin.site.register(SkillPower, SkillPowerAdmin)
admin.site.register(Feat, FeatAdmin)
