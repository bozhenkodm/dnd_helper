# Generated by Django 5.1.4 on 2024-12-14 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_propertiescondition_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertiescondition',
            name='constraint',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='scalar_conditions',
                to='base.constraint',
            ),
        ),
    ]
