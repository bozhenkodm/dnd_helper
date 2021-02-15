# Generated by Django 3.1.3 on 2021-02-14 15:42

from django.db import migrations


def class_names(apps, schema_editor):
    Class = apps.get_model('base', 'Class')
    Class.objects.filter(name='RUNEPRIEST_D').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20210214_1537'),
    ]

    operations = [migrations.RunPython(class_names)]
