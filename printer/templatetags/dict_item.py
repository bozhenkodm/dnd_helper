from django.template.defaultfilters import register


# @register.filter
def dictitem(dictionary, key):
    return dictionary.get(key)


register.filter(name='dictitem', filter_func=dictitem)
