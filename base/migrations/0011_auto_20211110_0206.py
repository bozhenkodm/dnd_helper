# Generated by Django 3.2.9 on 2021-11-10 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_attackpowerproperty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='const_bonus_attrs',
        ),
        migrations.RemoveField(
            model_name='race',
            name='fortitude_bonus',
        ),
        migrations.RemoveField(
            model_name='race',
            name='reflex_bonus',
        ),
        migrations.RemoveField(
            model_name='race',
            name='size',
        ),
        migrations.RemoveField(
            model_name='race',
            name='skill_bonuses',
        ),
        migrations.RemoveField(
            model_name='race',
            name='speed',
        ),
        migrations.RemoveField(
            model_name='race',
            name='var_bonus_attrs',
        ),
        migrations.RemoveField(
            model_name='race',
            name='vision',
        ),
        migrations.RemoveField(
            model_name='race',
            name='will_bonus',
        ),
    ]
