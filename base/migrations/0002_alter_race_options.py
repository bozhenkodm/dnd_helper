# Generated by Django 5.1.4 on 2025-01-01 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='race',
            options={
                'ordering': ('name_display',),
                'verbose_name': 'Race',
                'verbose_name_plural': 'Races',
            },
        ),
    ]