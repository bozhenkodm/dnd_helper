# Generated by Django 4.0.2 on 2022-02-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0011_alter_simplemagicitem_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='creation_step',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]