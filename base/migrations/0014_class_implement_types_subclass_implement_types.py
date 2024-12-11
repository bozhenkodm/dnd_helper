# Generated by Django 5.1.4 on 2024-12-10 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_rename_available_weapon_types_power_weapon_types_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='implement_types',
            field=models.ManyToManyField(
                limit_choices_to={'primary_end__isnull': True},
                related_name='implement_%(app_label)s_%(class)s_wielders',
                to='base.weapontype',
                verbose_name='Available weapon types',
            ),
        ),
        migrations.AddField(
            model_name='subclass',
            name='implement_types',
            field=models.ManyToManyField(
                limit_choices_to={'primary_end__isnull': True},
                related_name='implement_%(app_label)s_%(class)s_wielders',
                to='base.weapontype',
                verbose_name='Available weapon types',
            ),
        ),
    ]
