# Generated by Django 5.1.6 on 2025-02-17 19:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_availabilitycondition_book_source_class_book_source_and_more'),
        ('printer', '0002_alter_avatar_options_alter_gridmap_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='combatants',
            name='avatar',
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={'npc__isnull': True, 'pc__isnull': True},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='printer.avatar',
                verbose_name='Avatar',
            ),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='short_description',
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name='Short description'
            ),
        ),
    ]
