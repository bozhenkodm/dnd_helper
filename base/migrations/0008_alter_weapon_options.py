# Generated by Django 5.1.4 on 2025-02-14 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_magicitemtype_source'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weapon',
            options={'verbose_name': 'Weapon', 'verbose_name_plural': 'Weapons'},
        ),
    ]
