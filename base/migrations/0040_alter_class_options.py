# Generated by Django 4.0 on 2022-01-06 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_alter_class_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={
                'ordering': ('name_display',),
                'verbose_name': 'Класс',
                'verbose_name_plural': 'Классы',
            },
        ),
    ]
