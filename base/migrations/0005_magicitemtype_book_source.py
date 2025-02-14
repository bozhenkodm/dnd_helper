# Generated by Django 5.1.4 on 2025-02-14 08:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_book_options_alter_booksource_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='magicitemtype',
            name='book_source',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='base.booksource',
                verbose_name='Source',
            ),
        ),
    ]
