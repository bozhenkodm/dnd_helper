# Generated by Django 5.1.3 on 2024-11-29 21:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0037_alter_weapontype_second_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weapontype',
            name='second_end',
        ),
        migrations.AddField(
            model_name='weapontype',
            name='primary_end',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='base.weapontype',
                verbose_name='Primary end',
            ),
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='name',
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name='Title'
            ),
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='slug',
            field=models.CharField(
                blank=True, max_length=30, unique=True, verbose_name='Slug'
            ),
        ),
    ]
