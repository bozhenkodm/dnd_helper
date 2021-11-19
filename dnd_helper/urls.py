"""dnd_helper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from base.views import EncounterDetailView, MainView, NPCDetailView, NPCOldDetailView
from generator import views as generator_views
from printer.views import PrintableObjectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)


urlpatterns = [
    path('favicon.ico', favicon_view),
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main_view'),
    path(
        'generator/main',
        generator_views.GeneratorsMainView.as_view(),
        name='generator_main',
    ),
    path(
        'generator/tavern',
        generator_views.TavernView.as_view(),
        name='generator_tavern',
    ),
    path(
        'generator/tavern/<race>',
        generator_views.TavernView.as_view(),
        name='generator_tavern',
    ),
    path(
        'generator/fantasy_name',
        generator_views.FantasyNameView.as_view(),
        name='generator_fantasy_name',
    ),
    path(
        'generator/random_name',
        generator_views.RandomNameView.as_view(),
        name='random_fantasy_name',
    ),
    path('npc/detail/<pk>', NPCDetailView.as_view(), name='npc'),
    path('npc/detail/<pk>/old', NPCOldDetailView.as_view(), name='npc-old'),  # deprecated
    path('encounter/detail/<pk>', EncounterDetailView.as_view(), name='encounter'),
    path('printer/detail/<pk>', PrintableObjectView.as_view(), name='printer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
