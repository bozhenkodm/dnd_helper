from django.views.generic import DetailView

from printer.models import EncounterIcons, GridMap, PrintableObject


class PrintableObjectView(DetailView):
    model = PrintableObject


class EncounterIconsView(DetailView):
    model = EncounterIcons


class GridMapView(DetailView):
    model = GridMap

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        kwargs['participants'] = obj.get_participants_data()
        return super().get_context_data(**kwargs)
