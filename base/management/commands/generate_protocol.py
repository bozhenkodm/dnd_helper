import inspect
import os.path
from types import FunctionType
from typing import Any, ForwardRef

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
    help = 'Generate NPCProtocol'

    @staticmethod
    def create_django_protocol_code(model_cls: type, protocol_name: str) -> str:
        """
        Generates Protocol code for a Django model, including fields as Python types
        (e.g., CharField → str) and user-defined methods/properties.
        """
        imports: list[str] = [
            '# flake8: noqa',
            'from __future__ import annotations',
            'from typing import Protocol, Sequence, TYPE_CHECKING, Optional',
            'from django.db.models import Manager, QuerySet',
        ]
        code_lines = [f'class {protocol_name}(Protocol):']
        field_annotations = {}
        related_models: set[str] = set()
        model_classes: dict[str, type] = {}
        other_imports: set[str] = set()

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
                    model_classes[model_name] = related_model

                    if isinstance(field, models.ForeignKey):
                        type_str = f"'{model_name}'"
                    elif isinstance(field, models.ManyToManyField):
                        type_str = f"Manager['{model_name}']"
            else:
                # Handle scalar fields
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

        # Collect user-defined attributes from class hierarchy
        def is_model_attr(cls: type) -> bool:
            return any(
                issubclass(cls, parent) for parent in models.Model.__subclasses__()
            )

        attributes = {}
        for cls in model_cls.mro():
            if cls is models.Model or cls is object:
                continue
            for name, attr in cls.__dict__.items():
                if name.startswith('__') and name.endswith('__'):
                    continue
                if name in attributes:
                    continue
                if is_model_attr(cls):
                    continue
                attributes[name] = attr

        # Process methods and properties with safe annotation handling
        for name, attr in attributes.items():
            # Handle methods
            if isinstance(attr, FunctionType):
                try:
                    annotations = inspect.get_annotations(attr, eval_str=False)
                except AttributeError:
                    annotations = {}

                return_type = annotations.get('return', inspect.Parameter.empty)
                sig = inspect.signature(attr)

                # Build parameter list with model strings
                params = []
                for param in sig.parameters.values():
                    ann = annotations.get(param.name, param.annotation)
                    param_type = (
                        ann if ann is not param.empty else inspect.Parameter.empty
                    )

                    param_str = param.name
                    if param_type is not inspect.Parameter.empty:
                        # Handle ForwardRef and model references
                        if isinstance(param_type, ForwardRef):
                            param_str += f": '{param_type.__forward_arg__}'"
                        elif isinstance(param_type, str):
                            param_type = param_type.replace('typing.', '')
                            if '.' in param_type and not param_type.startswith(
                                'models.'
                            ):
                                parts = param_type.rsplit('.', 1)
                                if len(parts) == 2:
                                    module, type_name = parts
                                    other_imports.add(
                                        f'from {module} import {type_name}'
                                    )
                                    param_type = type_name
                            param_str += f": {param_type}"
                        elif inspect.isclass(param_type) and issubclass(
                            param_type, models.Model
                        ):
                            param_str += f": '{param_type.__name__}'"
                        else:
                            param_str += f": {param_type.__name__ if hasattr(param_type, '__name__') else param_type}"
                    if param.default is not param.empty:
                        param_str += f' = {param.default!r}'
                    params.append(param_str)

                params_str = ', '.join(params)

                # Handle return type
                return_str = ''
                if return_type is not inspect.Parameter.empty:
                    if isinstance(return_type, ForwardRef):
                        return_str = f" -> '{return_type.__forward_arg__}'"
                    elif isinstance(return_type, str):
                        return_type = return_type.replace('typing.', '')
                        if '.' in return_type and not return_type.startswith('models.'):
                            parts = return_type.rsplit('.', 1)
                            if len(parts) == 2:
                                module, type_name = parts
                                other_imports.add(f'from {module} import {type_name}')
                                return_type = type_name
                        return_str = f' -> {return_type}'
                    elif inspect.isclass(return_type) and issubclass(
                        return_type, models.Model
                    ):
                        return_str = f" -> '{return_type.__name__}'"
                    else:
                        return_str = f' -> {return_type.__name__ if hasattr(return_type, "__name__") else return_type}'
                code_lines.append(f'    def {name}({params_str}){return_str}: ...')

            # Handle properties
            elif isinstance(attr, property):
                return_type = inspect.Parameter.empty
                if attr.fget:
                    try:
                        annotations = inspect.get_annotations(attr.fget, eval_str=False)
                    except AttributeError:
                        annotations = {}
                    return_type = annotations.get('return', inspect.Parameter.empty)

                # Process return type
                if isinstance(return_type, ForwardRef):
                    return_type_str = f"'{return_type.__forward_arg__}'"
                elif isinstance(return_type, str):
                    return_type = return_type.replace('typing.', '')
                    if '.' in return_type and not return_type.startswith('models.'):
                        parts = return_type.rsplit('.', 1)
                        if len(parts) == 2:
                            module, type_name = parts
                            other_imports.add(f'from {module} import {type_name}')
                            return_type = type_name
                    return_type_str = return_type
                elif inspect.isclass(return_type) and issubclass(
                    return_type, models.Model
                ):
                    return_type_str = f"'{return_type.__name__}'"
                else:
                    return_type_str = (
                        return_type.__name__
                        if hasattr(return_type, '__name__')
                        else 'Any'
                    )
                code_lines.append(f'    @property')
                code_lines.append(f'    def {name}(self) -> {return_type_str}: ...')

        # Add non-model imports after initial imports
        imports[4:4] = sorted(other_imports)  # Insert after initial 4 imports

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
