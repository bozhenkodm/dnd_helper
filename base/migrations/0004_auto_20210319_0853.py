# Generated by Django 3.1.7 on 2021-03-19 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20210319_0853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='power',
            old_name='target_fkey',
            new_name='target',
        ),
    ]
