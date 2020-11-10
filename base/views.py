# Create your views here.
from django.views.generic import DetailView

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
