# Generated by Django 5.1.3 on 2024-11-30 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0043_alter_power_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weapontype',
            name='name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Title'),
        ),
    ]
