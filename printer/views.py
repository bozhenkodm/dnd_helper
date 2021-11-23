from django.views.generic import DetailView

from printer.models import PrintableObject


class PrintableObjectView(DetailView):
    model = PrintableObject
