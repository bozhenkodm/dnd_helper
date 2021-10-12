from django.views.generic import DetailView

from printer.models import PrintableObject


class PrintableObjectView(DetailView):
    model = PrintableObject
    # template_name = 'printer/printableobject_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     replaced_indexes = (
    #         random.randint(0, len(name) - 2) for _ in range(replaced_letter_number)
    #     )
    #     replacements = {}
    #     for i in replaced_indexes:
    #         if name[i] in vovels:
    #             replacements[i] = random.choice(vovels)
    #         else:
    #             replacements[i] = random.choice(consolants)
    #     name = ''.join(replacements.get(i, l) for i, l in enumerate(name)).capitalize()
    #     context['name'] = name
    #     return context
