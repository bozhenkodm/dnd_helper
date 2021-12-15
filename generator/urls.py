from django.urls import path

from generator.views import (
    FantasyNameView,
    GeneratorsMainView,
    RandomNameView,
    TavernView,
)

urlpatterns = [
    path(
        'main',
        GeneratorsMainView.as_view(),
        name='generator_main',
    ),
    path(
        'tavern',
        TavernView.as_view(),
        name='generator_tavern',
    ),
    path(
        'tavern/<race>',
        TavernView.as_view(),
        name='generator_tavern',
    ),
    path(
        'fantasy_name',
        FantasyNameView.as_view(),
        name='generator_fantasy_name',
    ),
    path(
        'random_name',
        RandomNameView.as_view(),
        name='random_fantasy_name',
    ),
]
