import io
import subprocess

from django.contrib import admin
from django.core.files.images import ImageFile
from django.utils.safestring import mark_safe

from printer.forms import EncounterIconForm
from printer.models import EncounterIcons, PrintableObject, PrintableObjectItems


class PrintableObjectItemsAdmin(admin.TabularInline):
    model = PrintableObjectItems


class PrintableObjectAdmin(admin.ModelAdmin):
    save_as = True
    enable_nav_sidebar = False
    readonly_fields = ('link',)
    inlines = (PrintableObjectItemsAdmin,)

    @admin.display(description='Лист для печати')
    def link(self, obj):
        if not obj or not obj.id:
            return '-'
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')


class EncounterIconsAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'link',
        'base_image',
        'upload_from_clipboard',
        'image_tag',
        'number',
        'number_color',
        'number_position',
    )
    readonly_fields = ('image_tag', 'link')
    # formfield_overrides = {forms.ChoiceField: {'widget': forms.RadioSelect}}
    form = EncounterIconForm

    @admin.display(description='Картинка')
    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.base_image.url}" />')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # TODO make a mixin with this method
        print(form.cleaned_data)
        if form.cleaned_data['upload_from_clipboard']:
            bashCommand = 'xclip -selection clipboard -t image/png -o'
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            image_field = ImageFile(io.BytesIO(output), name=f'Icon_{obj.id}.png')
            obj.base_image = image_field
            obj.save()

    @admin.display(description='Иконки с цифрами')
    def link(self, obj):
        if not obj or not obj.id:
            return '-'
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')


admin.site.register(PrintableObject, PrintableObjectAdmin)
admin.site.register(EncounterIcons, EncounterIconsAdmin)
