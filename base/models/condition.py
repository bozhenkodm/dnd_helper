from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Constraint(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'app_label': 'base',
            'model__in': (
                'Race',
                'Class',
                'FunctionalTemplate',
                'ParagonPath',
                'MagicItemType',
            ),
        },
    )
    object_id = models.PositiveIntegerField()
    belongs_to = GenericForeignKey("content_type", "object_id")


class Condition(models.Model):
    constraint = models.ForeignKey(Constraint, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'app_label': 'base',
            'model__in': (
                'Race',
                'Class',
                'FunctionalTemplate',
                'ParagonPath',
                'MagicItemType',
            ),
        },
    )
    object_id = models.PositiveIntegerField()
    condition = GenericForeignKey("content_type", "object_id")
