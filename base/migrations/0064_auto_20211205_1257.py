# Generated by Django 3.2.9 on 2021-12-05 12:57

from django.db import migrations, models


def migrate_power_properties(apps, schema_editor):
    PowerProperty = apps.get_model('base', 'PowerProperty')
    for pp in PowerProperty.objects.filter(title='OTHER'):
        pp.description = pp.description.replace('.', ':', 1)
        pp.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0063_auto_20211205_1145'),
    ]

    operations = [migrations.RunPython(migrate_power_properties)]
