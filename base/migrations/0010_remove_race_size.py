# Generated by Django 5.1.4 on 2024-12-29 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_race_size_int'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='size',
        ),
    ]
