# Generated by Django 5.1.7 on 2025-03-08 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_subclass_default_feats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='mandatory_skills',
            field=models.ManyToManyField(
                related_name='classes_for_mandatory',
                to='base.skill',
                verbose_name='Mandatory skills',
            ),
        ),
    ]
