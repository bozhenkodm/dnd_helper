from django.contrib import admin
from django.utils.safestring import mark_safe

from printer.models import PrintableObject, PrintableObjectItems


class PrintableObjectItemsAdmin(admin.StackedInline):
    model = PrintableObjectItems


class PrintableAdmin(admin.ModelAdmin):
    save_as = True
    enable_nav_sidebar = False
    readonly_fields = ('link',)
    inlines = (PrintableObjectItemsAdmin,)

    def link(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    link.short_description = 'Лист для печати'


admin.site.register(PrintableObject, PrintableAdmin)
