# Generated by Django 5.1.4 on 2024-12-23 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_skill_based_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skill',
            old_name='based_on_new',
            new_name='based_on',
        ),
    ]
