import json

from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from printer.forms import ParticipantPlaceForm
from printer.models import EncounterIcons, GridMap, ParticipantPlace, PrintableObject


class PrintableObjectView(DetailView):
    model = PrintableObject


class EncounterIconsView(DetailView):
    model = EncounterIcons


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
