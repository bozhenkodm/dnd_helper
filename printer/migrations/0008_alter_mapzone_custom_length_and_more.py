# Generated by Django 5.2 on 2025-04-13 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0007_rename_length_zone_default_length_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapzone',
            name='custom_length',
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name='Length'
            ),
        ),
        migrations.AlterField(
            model_name='mapzone',
            name='custom_width',
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name='Width'
            ),
        ),
    ]
