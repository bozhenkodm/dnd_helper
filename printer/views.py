from django.views.generic import DetailView

from printer.models import EncounterIcons, PrintableObject


class PrintableObjectView(DetailView):
    model = PrintableObject


class EncounterIconsView(DetailView):
    model = EncounterIcons
