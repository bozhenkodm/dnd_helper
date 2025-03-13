from typing import Any

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
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


class ControlPanelView(TemplateView):
    template_name = "base/control_panel.html"

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'cache_everything':
            for npc in NPC.objects.all():
                npc.cache_bonuses()
                print(f'{npc.name} bonuses has been cached')
                npc.cache_powers()
                print(f'{npc.name} power has been cached')
            messages.info(request, 'Cached')
            return HttpResponseRedirect(reverse('control_panel'))
        elif action == 'hello':
            messages.info(request, 'Hello!')
            return HttpResponseRedirect(reverse('control_panel'))
        else:
            messages.error(request, "Invalid action requested")
            return HttpResponseRedirect(reverse('control_panel'))


class MainView(TemplateView):
    template_name = 'base/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['links'] = (
            ('Генератор', reverse('generator_main')),
            ('Карты', reverse('gridmap_list')),
        )
        return context
