# Generated by Django 5.1.6 on 2025-02-22 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weaponstate',
            name='groups',
            field=models.ManyToManyField(
                blank=True, to='base.weapongroup', verbose_name='Weapon groups'
            ),
        ),
    ]
