from django.core import exceptions
from django.db.models import CharField
from django.template.defaultfilters import capfirst
from multiselectfield import MultiSelectFormField  # type: ignore
from multiselectfield.db.fields import MSFList  # type: ignore
from multiselectfield.utils import get_max_length, string_type  # type: ignore
from multiselectfield.validators import (  # type: ignore
    MaxChoicesValidator,
    MaxValueMultiFieldValidator,
    MinChoicesValidator,
)


class MultiSelectField(CharField):
    """Choice values can not contain commas."""

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        super(MultiSelectField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators.append(MaxValueMultiFieldValidator(self.max_length))
        if self.min_choices is not None:
            self.validators.append(MinChoicesValidator(self.min_choices))
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def get_choices_selected(self, arr_choices):
        named_groups = arr_choices and isinstance(arr_choices[0][1], (list, tuple))
        choices_selected = []
        if named_groups:
            for choice_group_selected in arr_choices:
                for choice_selected in choice_group_selected[1]:
                    choices_selected.append(string_type(choice_selected[0]))
        else:
            for choice_selected in arr_choices:
                choices_selected.append(string_type(choice_selected[0]))
        return choices_selected

    def value_to_string(self, obj) -> str:
        # try:
        #     value = self._get_val_from_obj(obj)
        # except AttributeError:
        value = super().value_from_object(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance) -> None:
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if opt_select not in arr_choices:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_choice'] % {"value": value}
                )

    def get_default(self):
        default = super(MultiSelectField, self).get_default()
        if isinstance(default, int):
            default = string_type(default)
        return default

    def formfield(self, **kwargs):
        defaults = {
            'required': not self.blank,
            'label': capfirst(self.verbose_name),
            'help_text': self.help_text,
            'choices': self.choices,
            'max_length': self.max_length,
            'max_choices': self.max_choices,
        }
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value) -> str:
        return '' if value is None else ','.join(map(str, value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared and not isinstance(value, string_type):
            value = self.get_prep_value(value)
        return value

    def to_python(self, value):
        choices = dict(self.flatchoices)

        if value:
            if isinstance(value, list):
                return value
            elif isinstance(value, string_type):
                value_list = map(
                    lambda x: x.strip(), value.replace(u'，', ',').split(',')
                )
                return MSFList(choices, value_list)
            elif isinstance(value, (set, dict)):
                return MSFList(choices, list(value))
        return MSFList(choices, [])

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:

            def get_list(obj):
                fieldname = name
                choicedict = dict(self.choices)
                display = []
                if getattr(obj, fieldname):
                    for value in getattr(obj, fieldname):
                        item_display = choicedict.get(value, None)
                        if item_display is None:
                            try:
                                item_display = choicedict.get(int(value), value)
                            except (ValueError, TypeError):
                                item_display = value
                        display.append(string_type(item_display))
                return display

            def get_display(obj):
                return ", ".join(get_list(obj))

            get_display.short_description = self.verbose_name

            setattr(cls, 'get_%s_list' % self.name, get_list)
            setattr(cls, 'get_%s_display' % self.name, get_display)
