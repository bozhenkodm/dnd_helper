# Generated by Django 3.2.9 on 2021-11-11 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20211110_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapontype',
            name='slug',
            field=models.CharField(max_length=20, null=True, verbose_name='Slug'),
        ),
    ]
