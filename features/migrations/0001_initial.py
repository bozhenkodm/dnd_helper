# Generated by Django 5.1.7 on 2025-03-18 08:38

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feat',
            fields=[],
            options={
                'verbose_name': 'Feat',
                'verbose_name_plural': 'Feats',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('base.feat',),
        ),
        migrations.CreateModel(
            name='Power',
            fields=[],
            options={
                'verbose_name': 'Power',
                'verbose_name_plural': 'Powers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('base.power',),
        ),
    ]
