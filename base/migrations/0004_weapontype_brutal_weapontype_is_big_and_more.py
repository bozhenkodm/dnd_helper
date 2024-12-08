# Generated by Django 5.1.3 on 2024-12-08 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_weapontype_dice_weapontype_dice_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapontype',
            name='brutal',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='weapontype',
            name='is_big',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='weapontype',
            name='is_defensive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='weapontype',
            name='is_high_crit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='weapontype',
            name='is_off_hand',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='weapontype',
            name='is_reach',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='weapontype',
            name='is_small',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='weapontype',
            name='load',
            field=models.CharField(
                choices=[('FREE', 'Свободное действие'), ('MINOR', 'Малое действие')],
                max_length=5,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='weapontype',
            name='thrown',
            field=models.CharField(
                choices=[('LIGHT', 'Лёгкое'), ('HEAVY', 'Тяжёлое')],
                max_length=5,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='dice',
            field=models.PositiveSmallIntegerField(
                choices=[(4, 'k4'), (6, 'k6'), (8, 'k8'), (10, 'k10'), (12, 'k12')],
                null=True,
            ),
        ),
    ]
