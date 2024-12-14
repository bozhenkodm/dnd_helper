# Generated by Django 5.1.4 on 2024-12-12 21:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_constraint_content_type_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='content_type',
            field=models.ForeignKey(
                limit_choices_to={
                    'app_label': 'base',
                    'model__in': (
                        'race',
                        'class',
                        'subclass',
                        'functionaltemplate',
                        'paragonpath',
                        'magicitemtype',
                        'feat',
                    ),
                },
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.contenttype',
            ),
        ),
        migrations.AlterField(
            model_name='constraint',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Name'),
        ),
    ]
