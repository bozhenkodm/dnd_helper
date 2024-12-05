from enum import Enum, IntEnum
from functools import reduce
from typing import Any, Callable, Self, Sequence

from django.db import models


class BaseNameValueDescriptionEnum(str, Enum):
    description: str

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    def _generate_next_value_(name, start, count, last_values):
        return str(name)

    @classmethod
    def generate_choices(
        cls,
        is_sorted: bool = True,
        start_with: Sequence[Self] = (),
        condition: Callable[[Any], bool] = lambda x: True,
        description_prefix: str = '',
    ) -> list[tuple[str, str]]:
        result = [(item.value, item.description) for item in start_with]  # type: ignore
        if is_sorted:
            result.extend(
                sorted(
                    (
                        (item.value, f'{description_prefix}{item.description}')
                        for item in cls
                        if item not in start_with and condition(item)
                    ),  # type: ignore
                    key=lambda x: x[1],
                )
            )
        else:
            result.extend(
                (item.value, f'{description_prefix}{item.description}')
                for item in cls
                if item not in start_with and condition(item)  # type: ignore
            )
        return result

    @classmethod
    def generate_case(cls, field='name') -> models.Case:
        kwargs = (
            {
                field: item.value,  # type: ignore[attr-defined]
                'then': models.Value(item.description),  # type: ignore[attr-defined]
            }
            for item in cls
        )
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.CharField())

    @classmethod
    def generate_order_case(cls, field='name') -> models.Case:
        kwargs = (
            {
                field: item.value,  # type: ignore[attr-defined]
                'then': models.Value(index),
            }
            for index, item in enumerate(cls)
        )
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.IntegerField())

    @classmethod
    def max_length(cls) -> int:
        return max(len(item.value) for item in cls)

    @classmethod
    def max_description_length(cls) -> int:
        return max(len(item.description) for item in cls)  # type: ignore[attr-defined]

    @property
    def lvalue(self) -> str:
        return self.value.lower()


class IntDescriptionEnum(IntEnum):
    description: str

    def __new__(cls, value, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def generate_choices(
        cls,
        condition: Callable[['IntDescriptionEnum'], bool] = lambda x: True,
    ):
        return sorted(
            ((item.value, item.description) for item in cls if condition(item)),
            key=lambda x: x[0],
        )

    @property
    def lname(self) -> str:
        return self.name.lower()

    @classmethod
    def generate_case(cls, field='name') -> models.Case:
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
    def generate_choices(cls):
        return sorted(
            [(item.value, item.description) for item in cls] + [(0, '---------')],
            key=lambda x: x[0],
        )


def generate_choices(
    *enums: type[BaseNameValueDescriptionEnum], is_sorted: bool = True
):
    return tuple(
        reduce(
            lambda x, y: x + y, (e.generate_choices(is_sorted=is_sorted) for e in enums)
        )
    )
