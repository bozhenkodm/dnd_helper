from django.contrib import admin

from generator.models import NPCName


class NameAdmin(admin.ModelAdmin):
    save_as = True
    enable_nav_sidebar = False

    def save_model(self, request, obj, form, change):
        obj.name = ' '.join(item.capitalize() for item in obj.name.split())
        try:
            ex_obj = self.model.objects.filter(name=obj.name)
        except self.model.DoesNotExist:
            # TODO add races processing
            pass
        return super().save_model(request, obj, form, change)


admin.site.register(NPCName, NameAdmin)
