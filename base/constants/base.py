from enum import Enum, IntEnum

from django.db import models


class BaseNameValueDescriptionEnum(str, Enum):
    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    def _generate_next_value_(name, start, count, last_values):
        return str(name)

    @classmethod
    def generate_choices(cls, is_sorted=True):
        if is_sorted:
            return sorted(
                ((item.value, item.description) for item in cls), key=lambda x: x[1]
            )
        return ((item.value, item.description) for item in cls)

    @classmethod
    def generate_case(cls, field='name'):
        kwargs = (
            {field: item.value, 'then': models.Value(item.description)} for item in cls
        )
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.CharField())

    @classmethod
    def generate_order_case(cls, field='name'):
        kwargs = (
            {field: item.value, 'then': models.Value(index)}
            for index, item in enumerate(cls)
        )
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.IntegerField())

    @classmethod
    def max_length(cls):
        # getting len(item.name) because auto() has no length
        return max(len(item.name) for item in cls)

    @property
    def lvalue(self):
        return self.value.lower()


class IntDescriptionEnum(IntEnum):
    def __new__(cls, value, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def generate_choices(cls):
        return sorted(
            ((item.value, item.description) for item in cls), key=lambda x: x[0]
        )

    @property
    def lname(self):
        return self.name.lower()

    @classmethod
    def generate_case(cls, field='name'):
        kwargs = ({field: item.name, 'then': models.Value(item.value)} for item in cls)
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.CharField())

    @classmethod
    def generate_value_description_case(cls, field='name'):
        kwargs = (
            {field: item.value, 'then': models.Value(item.description)} for item in cls
        )
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.CharField())


class IntDescriptionSubclassEnum(IntDescriptionEnum):
    @classmethod
    def generate_choices(cls, is_string_values=False):
        return sorted(
            [(item.value, item.description) for item in cls] + [(0, '---------')],
            key=lambda x: x[0],
        )
