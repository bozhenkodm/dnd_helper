from collections.abc import Callable, Iterable, Sequence
from enum import IntEnum, StrEnum
from itertools import chain
from typing import Any, Self

from django.db import models


class BaseNameValueDescriptionEnum(StrEnum):
    description: str

    def __new__(cls, value: str, description: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> str:
        return str(name)

    @classmethod
    def generate_choices(
        cls,
        *,
        is_sorted: bool = True,
        start_with: Sequence[Self] = (),
        condition: Callable[[Self], bool] = lambda x: True,
        description_prefix: str = '',
        zero_item: tuple[str, str] | None = None,
    ) -> list[tuple[str, str]]:
        result: list[tuple[str, str]] = [zero_item] if zero_item else []
        result.extend((item.value, item.description) for item in start_with)
        if is_sorted:
            result.extend(
                sorted(
                    (
                        (item.value, f'{description_prefix}{item.description}')
                        for item in cls
                        if item not in start_with and condition(item)
                    ),
                    key=lambda x: x[1],
                )
            )
        else:
            result.extend(
                (item.value, f'{description_prefix}{item.description}')
                for item in cls
                if item not in start_with and condition(item)
            )
        return result

    @classmethod
    def generate_case(cls, field: str = 'name') -> models.Case:
        kwargs = (
            {
                field: item.value,
                'then': models.Value(item.description),
            }
            for item in cls
        )
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.CharField())

    @classmethod
    def generate_order_case(cls, field: str = 'name') -> models.Case:
        kwargs = (
            {
                field: item.value,
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
        return max(len(item.description) for item in cls)

    @property
    def lvalue(self) -> str:
        return self.value.lower()

    @classmethod
    def get_by_description(cls, description: str, default: Self | None = None) -> Self:
        for member in cls:
            if member.description == description:
                return member
        if default is None:
            raise ValueError(f"Нет элемента с описанием '{description}'")
        return default


class IntDescriptionEnum(IntEnum):
    description: str

    def __new__(cls, value: int, description: str = '') -> Self:
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def get_by_description(cls, description: str) -> Self:
        for member in cls:
            if member.description == description:
                return member
        raise ValueError(f"Нет элемента с описанием '{description}'")

    @classmethod
    def generate_choices(
        cls,
        condition: Callable[[Self], bool] = lambda x: True,
        zero_item: tuple[int, str] | None = None,
    ) -> list[tuple[int, str]]:
        result: Iterable[tuple[int, str]] = (
            (item.value, item.description) for item in cls if condition(item)
        )
        if zero_item is not None:
            result = chain((zero_item,), result)
        return sorted(result, key=lambda x: x[0])

    @classmethod
    def generate_case(cls, field: str = 'name') -> models.Case:
        kwargs = ({field: item.name, 'then': models.Value(item.value)} for item in cls)
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.CharField())

    @classmethod
    def generate_value_description_case(cls, field: str = 'name') -> models.Case:
        kwargs = (
            {field: item.value, 'then': models.Value(item.description)} for item in cls
        )
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.CharField())
