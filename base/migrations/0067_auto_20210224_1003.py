# Generated by Django 3.1.3 on 2021-02-24 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0066_auto_20210224_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='racebonus',
            name='race',
        ),
        migrations.DeleteModel(
            name='ClassBonus',
        ),
        migrations.DeleteModel(
            name='RaceBonus',
        ),
    ]
