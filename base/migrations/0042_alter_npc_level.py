# Generated by Django 5.0.3 on 2024-03-15 20:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0041_npc_experience_alter_npc_trained_weapons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='level',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Level'),
        ),
    ]
