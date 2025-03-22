import inspect
import os.path
from types import FunctionType
from typing import Any, get_type_hints

from django.core.management import BaseCommand
from django.db import models

from base.models.models import NPC

DJANGO_FIELD_TO_PYTHON_TYPE = {
    models.AutoField: int,
    models.BigAutoField: int,
    models.CharField: str,
    models.TextField: str,
    models.IntegerField: int,
    models.BigIntegerField: int,
    models.BooleanField: bool,
    models.EmailField: str,
    models.FileField: str,
    models.ImageField: str,
    models.URLField: str,
    models.FloatField: float,
    models.ManyToManyField: models.Manager,
}


class Command(BaseCommand):
    help = 'Generate random abilities'

    @staticmethod
    def create_django_protocol_code(model_cls: type, protocol_name: str) -> str:
        """
        Generates Protocol code for a Django model, including fields as Python types
        (e.g., CharField → str) and user-defined methods/properties.
        """
        imports: list[str] = [
            '# flake8: noqa',
            'from __future__ import annotations',
            'from typing import Protocol, Iterable, Sequence, TYPE_CHECKING, Any',
            'from django.db.models import Manager',
        ]
        code_lines = [f'class {protocol_name}(Protocol):']
        field_annotations = {}
        related_models: set[str] = set()

        # Process model fields defined in the current class (not inherited)
        for field in model_cls._meta.get_fields():
            if not isinstance(field, models.Field):
                continue
            if getattr(field, 'model', None) != model_cls:
                continue  # Skip inherited fields

            python_type: Any = Any
            type_str = 'Any'

            # Handle ForeignKey/ManyToManyField (use string annotations)
            if isinstance(field, (models.ForeignKey, models.ManyToManyField)):
                related_model = field.remote_field.model
                if inspect.isclass(related_model) and issubclass(
                    related_model, models.Model
                ):
                    model_module = related_model.__module__
                    model_name = related_model.__name__
                    related_models.add(f'from {model_module} import {model_name}')

                    # Use string annotations for forward references
                    if isinstance(field, models.ForeignKey):
                        type_str = f"'{model_name}'"
                    elif isinstance(field, models.ManyToManyField):
                        type_str = f"Manager['{model_name}']"
            else:
                # Handle scalar fields (only in else block)
                for django_field, py_type in DJANGO_FIELD_TO_PYTHON_TYPE.items():
                    if isinstance(field, django_field):
                        python_type = py_type
                        type_str = python_type.__name__
                        break

            # Track standard library imports
            if isinstance(python_type, type):
                if python_type.__module__ == 'datetime':
                    imports.append('import datetime')
                elif python_type.__module__ == 'decimal':
                    imports.append('import decimal')
                elif python_type.__module__ == 'uuid':
                    imports.append('import uuid')

            field_annotations[field.name] = type_str

        # Add TYPE_CHECKING imports for related models
        if related_models:
            imports.append('if TYPE_CHECKING:')
            imports.extend(f'    {line}' for line in sorted(related_models))

        # Add field annotations to the protocol
        for field_name, type_str in field_annotations.items():
            code_lines.append(f'    {field_name}: {type_str}')

        # Process user-defined methods and properties
        for name, attr in model_cls.__dict__.items():
            if name.startswith('__') and name.endswith('__'):
                continue  # Skip special methods

            # Handle methods
            if isinstance(attr, FunctionType):
                sig = inspect.signature(attr)
                type_hints = get_type_hints(attr)
                return_type = type_hints.get('return', sig.return_annotation)

                # Build parameter list
                params = []
                for param in sig.parameters.values():
                    param_type = type_hints.get(param.name, param.annotation)
                    param_str = param.name
                    if param_type is not inspect.Parameter.empty:
                        param_type_str = (
                            param_type.__name__
                            if hasattr(param_type, '__name__')
                            else str(param_type)
                        )
                        param_str += f': {param_type_str}'
                    if param.default is not inspect.Parameter.empty:
                        param_str += f' = {param.default!r}'
                    params.append(param_str)

                params_str = ', '.join(params)
                return_str = (
                    f' -> {return_type.__name__}'
                    if return_type is not inspect.Parameter.empty
                    else ''
                )
                code_lines.append(f'    def {name}({params_str}){return_str}: ...')

            # Handle properties
            elif isinstance(attr, property):
                return_type = inspect.Parameter.empty
                if attr.fget:
                    type_hints = get_type_hints(attr.fget)
                    return_type = type_hints.get('return', inspect.Parameter.empty)

                return_type_str = (
                    return_type.__name__
                    if hasattr(return_type, '__name__')
                    else (
                        str(return_type)
                        if return_type is not inspect.Parameter.empty
                        else 'Any'
                    )
                )
                code_lines.append(f'    @property')
                code_lines.append(f'    def {name}(self) -> {return_type_str}: ...')

        # Add "pass" if no members
        if len(code_lines) == 1:
            code_lines.append('    pass')

        # Combine imports and protocol code
        imports_code = '\n'.join(imports)
        return f'{imports_code}\n\n' + '\n'.join(code_lines)

    def handle(self, *args, **options):

        with open(
            os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ),
                'models',
                'npc_protocol.py',
            ),
            'w',
        ) as f:
            f.write(self.create_django_protocol_code(NPC, 'NPCProtocol'))
        self.stdout.write(self.style.SUCCESS('Protocol generated. '))
