# Generated by Django 5.1.4 on 2025-01-27 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_power_frequency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='power',
            old_name='frequency_int',
            new_name='frequency',
        ),
    ]
