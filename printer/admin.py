import io
import subprocess

from django.contrib import admin, messages
from django.core.files.images import ImageFile
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL.Image import Transpose

from printer.forms import GridMapForm, ParticipantForm, ZoneForm
from printer.models import (
    Avatar,
    GridMap,
    MapZone,
    ParticipantPlace,
    PrintableObject,
    PrintableObjectItems,
    Zone,
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


class UploadFromClipboardModelAdmin(admin.ModelAdmin):
    IMAGE_FIELD_NAME = 'base_image'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if form.cleaned_data['upload_from_clipboard']:
            bashCommand = 'xclip -selection clipboard -t image/png -o'
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            image_field = ImageFile(io.BytesIO(output), name=f'Icon_{obj.id}.png')
            setattr(obj, self.IMAGE_FIELD_NAME, image_field)
            obj.save()


class ParticipantPlaceInline(admin.TabularInline):
    model = ParticipantPlace
    fields = ('participant', 'displayed_number', 'rotation', 'opacity', 'col', 'row')
    extra = 0


class ZonesInline(admin.TabularInline):
    model = MapZone
    extra = 0


class GridMapAdmin(UploadFromClipboardModelAdmin):
    inlines = (
        ParticipantPlaceInline,
        ZonesInline,
    )
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
                    (
                        'encounter',
                        'copy_from_map',
                    ),
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
        if encounter := form.cleaned_data.get('encounter'):
            if party := encounter.party:
                for pc in party.members.filter(avatar__isnull=False):
                    pps.append(
                        ParticipantPlace(
                            participant=pc.avatar, map=obj, row=row, col=col
                        )
                    )
                    col += pc.avatar.size
                for npc in party.npc_members.filter(avatar__isnull=False):
                    pps.append(
                        ParticipantPlace(
                            participant=npc.avatar, map=obj, row=row, col=col
                        )
                    )
                    col += npc.avatar.size
            col += 1
            if npcs := encounter.npcs:
                for npc in npcs.filter(avatar__isnull=False):
                    pps.append(
                        ParticipantPlace(
                            participant=npc.avatar, map=obj, row=row, col=col
                        )
                    )
                    col += npc.avatar.size
            for combatant in encounter.combatants_monsters.filter(
                monster__avatar__isnull=False
            ):
                for number in range(1, combatant.number + 1):
                    pps.append(
                        ParticipantPlace(
                            participant=combatant.monster.avatar,
                            map=obj,
                            row=row,
                            col=col,
                            # number 1 is not displayed
                            displayed_number=number if number > 1 else 0,
                        )
                    )
                    col += combatant.monster.avatar.size
            col += 1
        if copied_map := form.cleaned_data.get('copy_from_map'):
            for pp in copied_map.places.all():
                pps.append(
                    ParticipantPlace(
                        participant=pp.participant,
                        map=obj,
                        row=row,
                        col=col,
                        displayed_number=pp.displayed_number,
                    )
                )
                col += pp.participant.size

        if pps:
            ParticipantPlace.objects.bulk_create(pps)

        if form.cleaned_data.get('action') in Transpose and obj.base_image is not None:
            image = Image.open(obj.base_image.path)
            image = image.transpose(form.cleaned_data['action'])
            image.save(obj.base_image.path, format='png')
            obj.height = image.height
            obj.width = image.width
            obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == ParticipantPlace:
            is_updated = False
            # Track instances where `is_updated` is reset
            for form in formset.forms:
                # Skip invalid/deleted forms
                if not form.is_valid() or form.cleaned_data.get('DELETE', False):
                    continue

                instance = form.instance
                # Check if it's an existing instance (not new)
                if instance.pk:
                    # Check if `row`/`col` changed AND `is_updated` was originally True
                    if instance.is_updated and (
                        'row' in form.changed_data or 'col' in form.changed_data
                    ):
                        instance.is_updated = False
                        form.instance.refresh_from_db()
                        is_updated = True

            # Save the formset normally (includes our changes to `is_updated`)
            super().save_formset(request, form, formset, change)

            # Show message if changes occurred
            if is_updated:
                messages.warning(
                    request,
                    _(
                        'Some participants were moved on gridmap.'
                        ' Check coords and save again.'
                    ),
                )
        else:
            super().save_formset(request, form, formset, change)


class AvatarAdmin(UploadFromClipboardModelAdmin):
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


class ZoneAdmin(UploadFromClipboardModelAdmin):
    fields = (
        'name',
        'image',
        'upload_from_clipboard',
        'image_tag',
        'default_length',
        'default_width',
        'default_opacity',
    )
    readonly_fields = ('image_tag',)
    form = ZoneForm
    IMAGE_FIELD_NAME = 'image'

    @admin.display(description='Картинка')
    def image_tag(self, obj):
        return mark_safe(f'<img width=80px; height=auto; src="{obj.image.url}" />')


admin.site.register(PrintableObject, PrintableObjectAdmin)
admin.site.register(GridMap, GridMapAdmin)
admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Zone, ZoneAdmin)
