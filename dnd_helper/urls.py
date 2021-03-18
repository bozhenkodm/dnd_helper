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

from base.views import EncounterDetailView, MainView, NPCDetailView
from generator import views

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)


urlpatterns = [
    path('favicon.ico', favicon_view),
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main_view'),
    path('generator/main', views.GeneratorsMainView.as_view(), name='generator_main'),
    path('generator/tavern', views.TavernView.as_view(), name='generator_tavern'),
    path(
        'generator/tavern/<race>', views.TavernView.as_view(), name='generator_tavern'
    ),
    path(
        'generator/fantasy_name',
        views.FantasyNameView.as_view(),
        name='generator_fantasy_name',
    ),
    path('npc/detail/<pk>', NPCDetailView.as_view(), name='npc'),
    path('encounter/detail/<pk>', EncounterDetailView.as_view(), name='encounter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
