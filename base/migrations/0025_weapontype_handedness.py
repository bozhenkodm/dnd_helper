# Generated by Django 5.1.3 on 2024-11-27 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_magicweapontype_crit_dice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapontype',
            name='handedness',
            field=models.CharField(
                choices=[
                    ('two', 'Двуручное'),
                    ('free', 'Не занимает руки'),
                    ('one', 'Одноручное'),
                    ('versatile', 'Универсальное'),
                ],
                max_length=9,
                null=True,
                verbose_name='Handedness',
            ),
        ),
    ]
