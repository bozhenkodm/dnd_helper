# Generated by Django 4.0 on 2021-12-14 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_rename_enchantment_weapon_enchantment_old_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='power',
            name='accessory_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('TWO_WEAPONS', 'Два оружия'),
                    ('IMPLEMENT', 'Инструмент'),
                    ('WEAPON', 'Оружие'),
                ],
                max_length=11,
                null=True,
                verbose_name='Тип вооружения',
            ),
        ),
    ]
