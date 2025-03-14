# Generated by Django 5.1.7 on 2025-03-08 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_class_default_feats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subclass',
            name='default_feats',
            field=models.ManyToManyField(
                blank=True,
                related_name='subclasses',
                to='base.feat',
                verbose_name='Default feats',
            ),
        ),
    ]
