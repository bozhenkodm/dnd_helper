from typing import Any

from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, TemplateView

from base.constants.constants import SkillsEnum
from base.forms import EncounterChangeInitiativeForm
from base.models import NPC, Encounter
from base.models.encounter import EncounterParticipants


class NPCDetailView(DetailView):
    model = NPC

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        skills = (
            (item[1], getattr(obj, item[0].lower()))
            for item in SkillsEnum.generate_choices()
        )
        context['skills'] = skills
        return context


class EncounterDetailView(DetailView):
    model = Encounter

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(EncounterDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['change_initiative_form'] = EncounterChangeInitiativeForm(pk=obj.id)
        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if 'next_turn' in request.POST:
            obj.next_turn()
        elif 'previous_turn' in request.POST:
            obj.previous_turn()
        else:
            obj.roll_initiative()
        return self.get(request, *args, **kwargs)


class EncounterChangeInitiativeView(View):
    def post(self, request, *args, **kwargs):
        form = EncounterChangeInitiativeForm(request.POST, pk=kwargs.get('pk'))
        if form.is_valid():
            participant: EncounterParticipants = form.cleaned_data['participant']
            participant.move_after(form.cleaned_data['move_after'])

        return redirect('encounter', pk=kwargs.get('pk'))


class MainView(TemplateView):
    template_name = 'base/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['links'] = (('Генератор', reverse('generator_main')),)
        return context
