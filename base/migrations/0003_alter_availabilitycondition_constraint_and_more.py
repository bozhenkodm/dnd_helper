# Generated by Django 5.1.4 on 2024-12-26 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_availabilitycondition_default_feats_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabilitycondition',
            name='constraint',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='availability_conditions',
                to='base.constraint',
            ),
        ),
        migrations.DeleteModel(
            name='ArmamentCondition',
        ),
    ]