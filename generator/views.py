import random

from django.urls import reverse
from django.views.generic import TemplateView

from generator.constants import adjectives, nouns


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
        return context
