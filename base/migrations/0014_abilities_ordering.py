# Generated by Django 4.0.2 on 2022-02-15 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_abilities_alter_class_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='abilities',
            name='ordering',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
