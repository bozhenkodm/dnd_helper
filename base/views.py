from typing import Any

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView

from base.forms.encounter import EncounterChangeInitiativeForm
from base.forms.npc import NPCModelForm
from base.models.encounters import Encounter, EncounterParticipants, Party
from base.models.models import NPC


class NPCFormView(FormView):
    form_class = NPCModelForm
    template_name = 'base/npc_form.html'


class NPCListView(ListView):
    queryset = NPC.objects.order_by('-id')


class NPCDetailView(DetailView):
    model = NPC

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            obj.next_turn(request.POST)
        elif 'previous_turn' in request.POST:
            obj.previous_turn(request.POST)
        else:
            obj.roll_initiative()
        return self.get(request, *args, **kwargs)


class EncounterChangeInitiativeView(View):
    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = EncounterChangeInitiativeForm(request.POST, pk=kwargs.get('pk'))
        if form.is_valid():
            participant: EncounterParticipants = form.cleaned_data['participant']
            participant.move_after(form.cleaned_data['move_after'])

        return redirect('encounter', pk=kwargs.get('pk'))


class PCPartyView(DetailView):
    model = Party


class MainView(TemplateView):
    template_name = 'base/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['links'] = (
            ('Генератор', reverse('generator_main')),
            ('Карты', reverse('gridmap_list')),
        )
        return context
