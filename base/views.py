from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import DetailView, FormView, ListView, TemplateView

from base.forms.npc import NPCModelForm
from base.forms.power import FromImageForm
from base.models.encounters import Encounter, EncounterParticipants, Party
from base.models.models import NPC
from base.models.powers import Power


class NPCFormView(FormView):
    form_class = NPCModelForm
    template_name = 'base/npc_form.html'


class NPCListView(ListView):
    queryset = NPC.objects.order_by('-id')


class NPCDetailView(DetailView):
    model = NPC


class NPCPowerDetailView(DetailView):
    model = NPC
    template_name = 'base/npc_power_detail.html'

    def get_context_data(self, **kwargs):
        # Get the NPC object first (via DetailView's default logic)
        context = super().get_context_data(**kwargs)
        npc = self.object  # Already fetched NPC from URL's <pk>

        power_pk = self.kwargs['power_pk']
        power = get_object_or_404(npc.all_powers_qs(), pk=power_pk)
        # Add the Power to the template context
        context['powers'] = npc.powers_calculate((power,))
        return context


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


class PowerCreateFromImage(FormView):
    form_class = FromImageForm
    template_name = 'base/power_from_image.html'
    success_url = reverse_lazy('admin:features_classpower_add')

    def form_valid(self, form):
        self.json_data = Power.parse_from_image(form.cleaned_data['from_image'])
        return super().form_valid(form)

    def get_success_url(self):
        base_url = super().get_success_url()

        if hasattr(self, 'json_data') and isinstance(self.json_data, dict):
            # Преобразуем данные в query string
            params = urlencode(self.json_data, doseq=True)
            return f"{base_url}?{params}"

        return base_url


class MainView(TemplateView):
    template_name = 'base/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['links'] = (
            ('Генератор', reverse('generator_main')),
            ('Парсинг талантов', reverse('power_from_image')),
        )
        return context
