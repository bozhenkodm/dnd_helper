import io
import subprocess

from django.contrib import admin
from django.core.files.images import ImageFile
from django.utils.safestring import mark_safe
from PIL import Image
from PIL.Image import Transpose

from printer.forms import EncounterIconForm, GridMapForm, ParticipantForm
from printer.models import (
    Avatar,
    EncounterIcons,
    GridMap,
    ParticipantPlace,
    PrintableObject,
    PrintableObjectItems,
)


class PrintableObjectItemsAdmin(admin.TabularInline):
    model = PrintableObjectItems


class PrintableObjectAdmin(admin.ModelAdmin):
    save_as = True
    enable_nav_sidebar = False
    readonly_fields = ('link',)
    inlines = (PrintableObjectItemsAdmin,)

    @admin.display(description='Лист для печати', ordering='id')
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
    form = EncounterIconForm

    @admin.display(description='Картинка')
    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.base_image.url}" />')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # TODO make a mixin with this method
        if form.cleaned_data['upload_from_clipboard']:
            bashCommand = 'xclip -selection clipboard -t image/png -o'
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            image_field = ImageFile(io.BytesIO(output), name=f'Icon_{obj.id}.png')
            obj.base_image = image_field
            obj.save()

    @admin.display(description='Иконки с цифрами', ordering='id')
    def link(self, obj):
        if not obj or not obj.id:
            return '-'
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')


class ParticipantPlaceInline(admin.TabularInline):
    model = ParticipantPlace
    fields = ('participant', 'rotation', 'col', 'row')
    extra = 0


class GridMapAdmin(admin.ModelAdmin):
    inlines = (ParticipantPlaceInline,)
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'base_image',
                    'cells_on_longest_side',
                    'rows',
                    'cols',
                    'grid_color',
                    (
                        'upload_from_clipboard',
                        'action',
                    ),
                    'party',
                    'npcs',
                )
            },
        ),
        (
            'Картинка',
            {'fields': ('image_tag',), 'classes': ('collapse',)},
        ),
    )
    readonly_fields = ('image_tag', 'rows', 'cols')
    form = GridMapForm

    @admin.display(description='Картинка')
    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.base_image.url}" />')

    @admin.display(description='Количество строк')
    def rows(self, obj):
        if not obj.id:
            return '-'
        return obj.rows

    @admin.display(description='Количество столбцов')
    def cols(self, obj):
        if not obj.id:
            return '-'
        return obj.cols

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        row, col = 1, 1
        pps = []
        if party := form.cleaned_data.get('party'):
            for pc in party.members.filter(avatar__isnull=False):
                pps.append(
                    ParticipantPlace(participant=pc.avatar, map=obj, row=row, col=col)
                )
                col += 1
            for npc in party.npc_members.filter(avatar__isnull=False):
                pps.append(
                    ParticipantPlace(participant=npc.avatar, map=obj, row=row, col=col)
                )
                col += 1
        col += 1
        if npcs := form.cleaned_data.get('npcs'):
            for npc in npcs.all():
                pps.append(
                    ParticipantPlace(participant=npc.avatar, map=obj, row=row, col=col)
                )
                col += 1
        if pps:
            ParticipantPlace.objects.bulk_create(pps)

        # TODO make a mixin with this method
        if form.cleaned_data['upload_from_clipboard']:
            bashCommand = 'xclip -selection clipboard -t image/png -o'
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            image_field = ImageFile(io.BytesIO(output), name=f'Icon_{obj.id}.png')
            obj.base_image = image_field
            obj.save()

        if form.cleaned_data.get('action') in Transpose and obj.base_image is not None:
            image = Image.open(obj.base_image.path)
            image = image.transpose(form.cleaned_data['action'])
            image.save(obj.base_image.path, format='png')
            obj.height = image.height
            obj.width = image.width
            obj.save()


class AvatarAdmin(admin.ModelAdmin):
    fields = (
        'name',
        ('pc', 'npc'),
        'base_image',
        'base_size',
        'upload_from_clipboard',
        'image_tag',
    )
    readonly_fields = ('image_tag',)
    form = ParticipantForm
    autocomplete_fields = ('npc',)

    @admin.display(description='Картинка')
    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.base_image.url}" />')

    def save_model(self, request, obj, form, change):
        if not obj.name:
            if obj.pc:
                obj.name = obj.pc.name
            elif obj.npc:
                obj.name = obj.npc.name
        super().save_model(request, obj, form, change)
        # TODO make a mixin with this method
        if form.cleaned_data['upload_from_clipboard']:
            bashCommand = 'xclip -selection clipboard -t image/png -o'
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            image_field = ImageFile(io.BytesIO(output), name=f'Icon_{obj.id}.png')
            obj.base_image = image_field
            obj.save()


admin.site.register(PrintableObject, PrintableObjectAdmin)
admin.site.register(EncounterIcons, EncounterIconsAdmin)
admin.site.register(GridMap, GridMapAdmin)
admin.site.register(Avatar, AvatarAdmin)
