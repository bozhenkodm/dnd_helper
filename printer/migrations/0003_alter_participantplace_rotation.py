# Generated by Django 5.1.4 on 2024-12-30 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0002_remove_participantplace_is_unconscious_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantplace',
            name='rotation',
            field=models.PositiveSmallIntegerField(
                choices=[(0, 0), (90, 90), (180, 180), (270, 270)], default=0
            ),
        ),
    ]
