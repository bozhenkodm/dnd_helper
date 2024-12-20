# Generated by Django 5.1.4 on 2024-12-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_remove_weaponstate_is_reach_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bonus',
            name='item_condition',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='is_big',
        ),
        migrations.RemoveField(
            model_name='weapontype',
            name='is_off_hand',
        ),
        migrations.AddField(
            model_name='availabilitycondition',
            name='default_feats',
            field=models.ManyToManyField(
                blank=True, to='base.feat', verbose_name='Default feats'
            ),
        ),
        migrations.AddField(
            model_name='class',
            name='default_feats',
            field=models.ManyToManyField(
                blank=True, to='base.feat', verbose_name='Default feats'
            ),
        ),
        migrations.AddField(
            model_name='subclass',
            name='default_feats',
            field=models.ManyToManyField(
                blank=True, to='base.feat', verbose_name='Default feats'
            ),
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='handedness',
            field=models.CharField(
                choices=[
                    ('OFF_HAND', 'Дополнительное'),
                    ('ONE', 'Одноручное'),
                    ('VERSATILE', 'Универсальное'),
                    ('TWO', 'Двуручное'),
                    ('FREE', 'Не занимает руки'),
                ],
                max_length=9,
                verbose_name='Handedness',
            ),
        ),
    ]
