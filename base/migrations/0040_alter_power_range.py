# Generated by Django 3.2.9 on 2021-11-22 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_auto_20211122_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='power',
            name='range',
            field=models.SmallIntegerField(default=0, verbose_name='Дальность'),
        ),
    ]