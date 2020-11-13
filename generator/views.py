import random

from django.urls import reverse
from django.views.generic import TemplateView

from generator.constants import adjectives, nouns
from generator.models import NPCName


class GeneratorsMainView(TemplateView):
    template_name = 'generator/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tavern_url = reverse('generator_tavern')
        context['tavern_url'] = tavern_url
        return context


class TavernView(TemplateView):
    template_name = 'generator/tavern.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tavern = f'{random.choice(adjectives.split()).capitalize()} {random.choice(nouns.split()).capitalize()}'
        context['tavern'] = tavern
        taverner = NPCName.generate_taverner()
        context['taverner_first_name'] = taverner['first_name']
        context['taverner_last_name'] = taverner['last_name']
        context['taverner_sex'] = taverner['sex']
        context['taverner_race'] = taverner['race']
        return context
