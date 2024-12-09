from typing import Any

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, TemplateView

from base.constants.constants import SkillEnum
from base.forms.encounter import EncounterChangeInitiativeForm
from base.forms.npc import NPCModelForm
from base.models import NPC, Encounter
from base.models.encounters import EncounterParticipants, PCParty
from base.models.klass import Class
from base.objects import npc_klasses


class SubclassOptionsView(View):
    def get(self, request, *args, **kwargs):
        klass_id = request.GET.get('klass')
        try:
            klass = Class.objects.get(id=klass_id)
        except (Class.DoesNotExist, ValueError):
            return JsonResponse({})
        klass_instance = npc_klasses.get(klass.name)
        if not klass_instance:
            return JsonResponse({})
        subclass_enum = klass_instance.SubclassEnum
        return JsonResponse(dict(subclass_enum.generate_choices()))


class NPCFormView(FormView):
    form_class = NPCModelForm
    template_name = 'base/npc_form.html'


class NPCDetailView(DetailView):
    model = NPC

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        skills = (
            (item[1], getattr(obj, item[0].lower()))
            for item in SkillEnum.generate_choices()
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
    model = PCParty


class MainView(TemplateView):
    template_name = 'base/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['links'] = (('Генератор', reverse('generator_main')),)
        return context
