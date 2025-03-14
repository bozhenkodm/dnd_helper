# Generated by Django 5.1.7 on 2025-03-08 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_class_mandatory_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='trained_skills',
            field=models.ManyToManyField(
                blank=True,
                related_name='npcs',
                to='base.skill',
                verbose_name='Trained skills',
            ),
        ),
    ]
