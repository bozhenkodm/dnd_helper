from django.contrib import admin

from generator.models import NPCName


class NameAdmin(admin.ModelAdmin):
    save_as = True
    enable_nav_sidebar = False


admin.site.register(NPCName, NameAdmin)
