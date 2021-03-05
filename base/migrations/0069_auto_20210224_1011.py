# Generated by Django 3.1.3 on 2021-02-24 10:11

from django.db import migrations


def migrate(apps, schema_editor):
    Power = apps.get_model('base', 'Power')
    Power.objects.filter(frequency='PASSIVE').update(dice_number=0)


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0068_auto_20210224_1009'),
    ]

    operations = [migrations.RunPython(migrate)]
