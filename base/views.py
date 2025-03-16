from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView, TemplateView

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

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if 'next_turn' in request.POST:
            obj.next_turn(request.POST)
        elif 'previous_turn' in request.POST:
            obj.previous_turn(request.POST)
        elif 'kill_participant' in request.POST:
            participant_id = request.POST.get('participant_id')
            participant = EncounterParticipants.objects.get(id=participant_id)
            participant.is_active = False
            participant.save()
        elif 'unkill_participant' in request.POST:
            participant_id = request.POST.get('participant_id')
            participant = EncounterParticipants.objects.get(id=participant_id)
            participant.is_active = True
            participant.save()
        elif 'move_after' in request.POST:
            participant_id = request.POST.get('participant_id')
            move_after_id = request.POST.get("move_after_id")
            if participant_id and move_after_id:
                try:
                    participant = EncounterParticipants.objects.get(id=participant_id)
                    target = EncounterParticipants.objects.get(id=move_after_id)
                    participant.move_after(target)
                except (EncounterParticipants.DoesNotExist, ValueError):
                    pass
        else:
            obj.roll_initiative()
        return self.get(request, *args, **kwargs)


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
