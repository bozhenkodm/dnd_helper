# Generated by Django 4.0 on 2022-01-06 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0037_alter_class_options_rename_slug_class_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='name_display',
            field=models.CharField(max_length=15, verbose_name='Название'),
        ),
    ]