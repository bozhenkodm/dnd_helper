# Generated by Django 4.2.4 on 2023-08-05 13:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0034_alter_class_name_alter_power_frequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='owner',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]