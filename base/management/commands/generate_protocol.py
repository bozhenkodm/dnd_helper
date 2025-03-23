import inspect
import os.path
from types import FunctionType
from typing import Any, ForwardRef, Set, Union, get_args, get_origin

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
        imports: Set[str] = set({'from typing import TYPE_CHECKING'})
        typing_imports: Set[str] = set()
        fields_code = []

        def process_annotation(annotation: Any) -> str:
            nonlocal imports, typing_imports
            if annotation is inspect.Parameter.empty:
                return ''

            # Handle ForwardRefs and string annotations
            if isinstance(annotation, ForwardRef):
                return f"'{annotation.__forward_arg__}'"
            if isinstance(annotation, str):
                return f"'{annotation}'"

            # Handle generic types from typing
            origin = get_origin(annotation)
            if origin:
                args = get_args(annotation)
                origin_name = (
                    origin.__name__ if hasattr(origin, '__name__') else str(origin)
                )
                if origin not in (Union, tuple):
                    typing_imports.add(origin_name)
                processed_args = ', '.join(process_annotation(arg) for arg in args)
                return f"{origin_name}[{processed_args}]"

            # Handle regular types
            if isinstance(annotation, type):
                if annotation.__module__ == 'builtins':
                    return annotation.__name__
                imports.add(
                    f'from {annotation.__module__} import {annotation.__name__}'
                )
                return f"'{annotation.__name__}'"

            return str(annotation)

        # Process fields
        for field in model_cls._meta.fields + model_cls._meta.many_to_many:
            if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                related_model = field.related_model
                if related_model:
                    imports.add(
                        f'from {related_model.__module__} import {related_model.__name__}'
                    )
                    field_type = f"'{related_model.__name__}'"
                else:
                    field_type = 'Any'
                    typing_imports.add('Any')
            elif isinstance(field, models.ManyToManyField):
                related_model = field.related_model
                if related_model:
                    imports.add(
                        f'from {related_model.__module__} import {related_model.__name__}'
                    )
                    imports.add('from django.db.models import Manager')
                    field_type = f"'Manager[{related_model.__name__}]'"
                else:
                    field_type = 'Any'
                    typing_imports.add('Any')
            else:
                python_type = DJANGO_FIELD_TO_PYTHON_TYPE.get(field.__class__, Any)
                if python_type is Any:
                    typing_imports.add('Any')
                field_type = process_annotation(python_type)
            fields_code.append(f'    {field.name}: {field_type}')

        methods_code = []
        properties_code = []

        # Process methods and properties
        for name, member in inspect.getmembers(model_cls):
            if name.startswith('_'):
                continue

            # Handle static methods
            if isinstance(member, staticmethod):
                try:
                    sig = inspect.signature(member.__func__)
                except ValueError:
                    continue

                params = []
                for param in sig.parameters.values():
                    ann_str = process_annotation(param.annotation)
                    param_str = f'{param.name}: {ann_str}' if ann_str else param.name
                    if param.default is not inspect.Parameter.empty:
                        param_str += ' = ...'
                    params.append(param_str)

                return_ann = process_annotation(sig.return_annotation)
                return_str = f' -> {return_ann}' if return_ann else ''
                methods_code.append(
                    f'    @staticmethod\n    def {name}({", ".join(params)}){return_str}: ...'
                )
                continue

            # Handle regular methods
            if isinstance(member, FunctionType):
                try:
                    sig = inspect.signature(member)
                except ValueError:
                    continue

                params = []
                for param in sig.parameters.values():
                    if param.name == 'self':
                        params.append('self')
                        continue
                    ann_str = process_annotation(param.annotation)
                    param_str = f'{param.name}: {ann_str}' if ann_str else param.name
                    if param.default is not inspect.Parameter.empty:
                        param_str += ' = ...'
                    params.append(param_str)

                return_ann = process_annotation(sig.return_annotation)
                return_str = f' -> {return_ann}' if return_ann else ''
                methods_code.append(
                    f'    def {name}({", ".join(params)}){return_str}: ...'
                )

            # Handle properties
            elif isinstance(member, property):
                fget = member.fget
                if fget:
                    try:
                        sig = inspect.signature(fget)
                        return_ann = process_annotation(sig.return_annotation)
                        properties_code.append(
                            f'    @property\n    def {name}(self) -> {return_ann}: ...'
                        )
                    except (ValueError, AttributeError):
                        continue

        # Build final code
        code_lines = ['from typing import Protocol, TYPE_CHECKING']

        # Add typing imports if needed
        if typing_imports:
            code_lines.append(f'from typing import {", ".join(sorted(typing_imports))}')

        code_lines.append('\nif TYPE_CHECKING:')
        code_lines.extend(f'    {imp}' for imp in sorted(imports))

        code_lines.append(f'\nclass {protocol_name}(Protocol):')
        if not fields_code and not methods_code and not properties_code:
            code_lines.append('    pass')
        else:
            code_lines.extend(fields_code)
            code_lines.extend(methods_code)
            code_lines.extend(properties_code)

        # Add ForwardRef import if used
        if any('ForwardRef' in line for line in code_lines):
            code_lines.insert(1, 'from typing import ForwardRef')

        return '\n'.join(code_lines)

    def handle(self, *args, **options):
        output_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            'models',
            'npc_protocol.py',
        )
        with open(output_path, 'w') as f:
            f.write(self.create_django_protocol_code(NPC, 'NPCProtocol'))
        self.stdout.write(self.style.SUCCESS('Protocol generated successfully.'))
