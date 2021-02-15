# Generated by Django 3.1.3 on 2021-02-15 09:58

from django.db import migrations

from base.constants.constants import WeaponCategoryIntEnum


def category_migrate(apps, schema_editor):
    Class = apps.get_model('base', 'Class')
    for w_type in Class.objects.all():
        w_type.available_weapon_categories_int = [
            WeaponCategoryIntEnum(category)
            for category in w_type.available_weapon_categories
        ]
        w_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_auto_20210215_0958'),
    ]

    operations = [migrations.RunPython(category_migrate)]