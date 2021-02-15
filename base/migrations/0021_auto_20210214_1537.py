# Generated by Django 3.1.3 on 2021-02-14 15:37

from django.db import migrations


def class_names(apps, schema_editor):
    Class = apps.get_model('base', 'Class')
    Class.objects.filter(name='RUNEPRIEST_W').update(name='RUNEPRIEST')


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_auto_20210214_1536'),
    ]

    operations = [migrations.RunPython(class_names)]
