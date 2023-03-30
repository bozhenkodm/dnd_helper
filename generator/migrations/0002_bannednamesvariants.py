# Generated by Django 4.1.6 on 2023-03-27 05:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannedNamesVariants',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=30, unique=True, verbose_name='Имя'),
                ),
            ],
        ),
    ]
