import random

from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from generator.constants import adjectives, consolants, names, nouns, vovels
from generator.forms import NPCNameForm
from generator.models import NPCName


class GeneratorsMainView(TemplateView):
    template_name = 'generator/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['npc_url'] = reverse('generator_npc')
        context['tavern_url'] = reverse('generator_tavern')
        context['fantasy_name_url'] = reverse('generator_fantasy_name')
        context['random_name_url'] = reverse('random_fantasy_name')
        return context


class NpcGeneratorView(TemplateView):
    template_name = 'generator/npc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sex = self.request.GET.get('sex')
        race = kwargs.get('race')
        if race:
            race = race.upper()
        npc = NPCName.generate_npc(race, sex)
        context['first_name'] = npc['first_name']
        context['last_name'] = npc['last_name']
        context['sex'] = npc['sex']
        context['race'] = npc['race'].get_name_display()
        context['links'] = [
            ('Все расы', reverse('generator_npc'))
        ] + NPCName.generate_links()

        query_params = {
            'name': (
                ' '.join((npc['first_name'], npc['last_name']))
                if npc['last_name']
                else npc['first_name']
            ),
            'sex': npc['sex'],
            'race': npc['race'].id,
        }

        context['npc_create_link_admin'] = (
            reverse('admin:base_npc_add')
            + '?'
            + '&'.join((f'{name}={value}' for name, value in query_params.items()))
        )
        context['npc_create_link'] = (
            reverse('npc_create')
            + '?'
            + '&'.join((f'{name}={value}' for name, value in query_params.items()))
        )

        return context


class TavernView(TemplateView):
    template_name = 'generator/tavern.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tavern = (
            f'{random.choice(adjectives.split()).capitalize()}'
            f' {random.choice(nouns.split()).capitalize()}'
        )
        context['tavern'] = tavern
        return context


class GenerateNameFormView(FormView):
    template_name = 'generator/fantasy_name.html'
    form_class = NPCNameForm

    name = ''

    def generate_name(self) -> str:
        return self.name

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.generate_name()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.generate_name()
        return context


class FantasyNameView(GenerateNameFormView):
    success_url = reverse_lazy('generator_fantasy_name')

    def generate_name(self) -> str:
        if self.name:
            return self.name
        name = random.choice(list(names)).lower()
        replaced_letter_number = random.randint(0, 2)
        replaced_indexes = (
            random.randint(0, len(name) - 2) for _ in range(replaced_letter_number)
        )
        replacements = {}
        for i in replaced_indexes:
            if name[i] in vovels:
                replacements[i] = random.choice(vovels)
            else:
                replacements[i] = random.choice(consolants)
        self.name = ''.join(
            replacements.get(i, l) for i, l in enumerate(name)
        ).capitalize()
        return self.name


class RandomNameView(GenerateNameFormView):
    vovels = 'аеиоуэ'
    consolants = 'бвгджзклмнпрстфхцчш'
    success_url = reverse_lazy('random_fantasy_name')

    def generate_name(self) -> str:
        if self.name:
            return self.name
        self.name = ''.join(
            self.get_syllable() for _ in range(random.randint(1, 4))
        ).capitalize()
        return self.name

    def get_syllable(self):
        return (
            f'{random.choice(self.consolants)}'
            f'{random.choice(self.vovels)}'
            f'{random.randint(False, True) * random.choice(self.consolants)}'
        )
