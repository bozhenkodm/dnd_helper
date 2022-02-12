# Generated by Django 4.0.2 on 2022-02-12 17:16

from django.db import migrations, models

import base.constants.constants


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_handsslotitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handsslotitem',
            name='shield',
            field=models.SmallIntegerField(
                choices=[(0, '----------'), (1, 'Лёгкий щит'), (2, 'Тяжелый щит')],
                default=base.constants.constants.ShieldTypeIntEnum['NONE'],
                verbose_name='Shield',
            ),
        ),
    ]
