from django.urls import path

from printer.views import EncounterIconsView, PrintableObjectView

urlpatterns = [
    path(
        'printable_object/<pk>', PrintableObjectView.as_view(), name='printable_object'
    ),
    path('encounter_icon/<pk>', EncounterIconsView.as_view(), name='encounter_icon'),
]
