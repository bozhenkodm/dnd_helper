import random

from django.urls import reverse
from django.views.generic import TemplateView

from generator.constants import adjectives, consolants, names, nouns, vovels
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
        context = super().get_context_data(**kwargs)
        tavern = f'{random.choice(adjectives.split()).capitalize()} {random.choice(nouns.split()).capitalize()}'
        context['tavern'] = tavern
        race = kwargs.get('race')
        if race:
            race = race.upper()
        taverner = NPCName.generate_taverner(race)
        context['taverner_first_name'] = taverner['first_name']
        context['taverner_last_name'] = taverner['last_name']
        context['taverner_sex'] = taverner['sex']
        context['taverner_race'] = taverner['race']
        context['links'] = [('Все расы', reverse('generator_tavern'))] + [
            (
                race.value,
                reverse('generator_tavern', kwargs={'race': race.name.lower()}),
            )
            for race in NPCName.generate_links()
        ]
        return context


class FantasyNameView(TemplateView):
    template_name = 'generator/fantasy_name.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = random.choice(names.split()).lower()
        replaced_letter_number = random.randint(1, 2)
        replaced_indexes = (
            random.randint(0, len(name) - 2) for _ in range(replaced_letter_number)
        )
        replacements = {}
        for i in replaced_indexes:
            if name[i] in vovels:
                replacements[i] = random.choice(vovels)
            else:
                replacements[i] = random.choice(consolants)
        name = ''.join(replacements.get(i, l) for i, l in enumerate(name)).capitalize()
        context['name'] = name
        return context
