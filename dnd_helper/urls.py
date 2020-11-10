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
from django.contrib import admin
from django.urls import path

from base.views import EncounterDetailView, NPCDetailView
from generator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generator/main', views.GeneratorsMainView.as_view(), name='generator_main'),
    path('generator/tavern', views.TavernView.as_view(), name='generator_tavern'),
    path('npc/detail/<pk>', NPCDetailView.as_view(), name='npc'),
    path('encounter/detail/<pk>', EncounterDetailView.as_view(), name='encounter'),
]
