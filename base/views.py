# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, TemplateView

from base.constants import SkillsEnum
from base.models import NPC, Encounter


class NPCDetailView(DetailView):
    model = NPC

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        skills = (
            (item[1], getattr(object, item[0].lower()))
            for item in SkillsEnum.generate_choices()
        )
        context['skills'] = skills
        return context


class EncounterDetailView(DetailView):
    model = Encounter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skills = {item.name: item.value for item in SkillsEnum}
        context['skills'] = skills
        return context


class MainView(TemplateView):
    template_name = 'base/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['links'] = (('Генератор', reverse('generator_main')),)
        return context
