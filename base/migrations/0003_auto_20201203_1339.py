# Generated by Django 3.1.3 on 2020-12-03 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20201201_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='implement_attack_attributes',
        ),
        migrations.RemoveField(
            model_name='class',
            name='weapon_attack_attributes',
        ),
    ]
