# Generated by Django 5.1.4 on 2024-12-23 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_remove_npc_trained_skills'),
    ]

    operations = [
        migrations.RenameField(
            model_name='npc',
            old_name='trained_skills_new',
            new_name='trained_skills',
        ),
    ]
