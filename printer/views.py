from django.views.generic import DetailView

from printer.models import EncounterIcons, GridMap, PrintableObject


class PrintableObjectView(DetailView):
    model = PrintableObject


class EncounterIconsView(DetailView):
    model = EncounterIcons


class GridMapView(DetailView):
    model = GridMap
