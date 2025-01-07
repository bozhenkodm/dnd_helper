from django.urls import path

from printer.views import (
    EncounterIconsView,
    GridMapEditView,
    GridMapListView,
    GridMapView,
    PrintableObjectView,
)

urlpatterns = [
    path(
        'printable_object/<int:pk>',
        PrintableObjectView.as_view(),
        name='printable_object',
    ),
    path(
        'encounter_icon/<int:pk>', EncounterIconsView.as_view(), name='encounter_icon'
    ),
    path('gridmap/', GridMapListView.as_view(), name='gridmap_list'),
    path('gridmap/<int:pk>', GridMapView.as_view(), name='gridmap'),
    path('gridmap/<int:pk>/edit/', GridMapEditView.as_view(), name='gridmap_edit'),
]
