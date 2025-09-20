import json
import re

from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from base.objects.dice import DiceRoll
from printer.forms import ParticipantPlaceForm
from printer.models import GridMap, ParticipantPlace, PrintableObject, Song


class PrintableObjectView(DetailView):
    model = PrintableObject


class GridMapListView(ListView):
    model = GridMap
    ordering = ('-id',)


class GridMapView(DetailView):
    model = GridMap


class GridMapEditView(View):
    template_name = "printer/gridmap_edit.html"

    def get(self, request, *args, **kwargs):
        grid_map = get_object_or_404(GridMap, pk=self.kwargs['pk'])
        ParticipantPlaceFormSet = inlineformset_factory(
            GridMap, ParticipantPlace, form=ParticipantPlaceForm, extra=0
        )
        formset = ParticipantPlaceFormSet(instance=grid_map)
        return render(
            request, self.template_name, {'formset': formset, 'grid_map': grid_map}
        )

    def post(self, request, *args, **kwargs):
        grid_map = get_object_or_404(GridMap, pk=self.kwargs['pk'])
        ParticipantPlaceFormSet = inlineformset_factory(
            GridMap, ParticipantPlace, form=ParticipantPlaceForm, extra=0
        )
        formset = ParticipantPlaceFormSet(request.POST, instance=grid_map)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(
                reverse('gridmap_edit', kwargs={'pk': self.kwargs['pk']})
            )

        return render(
            request, self.template_name, {'formset': formset, 'grid_map': grid_map}
        )


class GridMapUpdateCoordsView(View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode())
        grid_map = get_object_or_404(GridMap, pk=self.kwargs['pk'])
        remnants_number = grid_map.move_participant(
            body['participant_id'], body['new_row'], body['new_col']
        )
        return JsonResponse(
            {
                'status': 'ok',
                'remnants': remnants_number > 0,
            }
        )


class SongView(View):

    def get(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        lines = []
        if song.manual_mode:
            lines.append({'text': '', 'delay': 0})

        for line in song.lyrics.split('\n'):
            line = line.strip()
            parts = line.rsplit('|', 1)
            text = parts[0].strip()
            delay = int(parts[1]) if len(parts) > 1 else 1000
            lines.append({'text': text, 'delay': delay})

        return render(
            request,
            'printer/song.html',
            {'song': song, 'lines': lines, 'auto_mode': song.auto_mode},
        )


class DiceRollView(View):
    template_name = 'printer/dice_roll.html'

    def parse_dice_expression(self, expression):
        expression = expression.replace(' ', '').lower()

        dice_pattern = r'(\d*)([dk])(\d+)'
        number_pattern = r'(?<![dk])(?<!\d)(\d+)(?![dk])'

        dice_matches = re.findall(dice_pattern, expression)
        number_matches = re.findall(number_pattern, expression)

        total_result = 0
        roll_details = []

        for num_str, d_char, sides_str in dice_matches:
            num_dice = int(num_str) if num_str else 1
            sides = int(sides_str)

            try:
                dice_roll = DiceRoll.from_str(f"{num_dice}d{sides}")
                result = dice_roll.roll()
                total_result += result
                roll_details.append(
                    {'expression': f"{num_dice}d{sides}", 'result': result}
                )
            except (ValueError, KeyError):
                pass

        for num_str in number_matches:
            modifier = int(num_str)
            total_result += modifier
            roll_details.append({'expression': f"+{modifier}", 'result': modifier})

        return total_result, roll_details

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        expression = request.POST.get('expression', '').strip()

        if not expression:
            return render(
                request, self.template_name, {'error': 'Please enter a dice expression'}
            )

        try:
            total, details = self.parse_dice_expression(expression)

            return render(
                request,
                self.template_name,
                {'expression': expression, 'total': total, 'details': details},
            )
        except Exception as e:
            return render(
                request,
                self.template_name,
                {
                    'expression': expression,
                    'error': f'Invalid dice expression: {str(e)}',
                },
            )
