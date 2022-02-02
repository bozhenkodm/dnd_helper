# Generated by Django 4.0.1 on 2022-01-27 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_armsslotitem_feetslotitem_handsslotitem_headslotitem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='arms_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_arms',
                to='base.armsslotitem',
                verbose_name='Предмет на предплечья',
            ),
        ),
        migrations.AddField(
            model_name='npc',
            name='feet_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_feet',
                to='base.feetslotitem',
                verbose_name='Предмет на ноги',
            ),
        ),
        migrations.AddField(
            model_name='npc',
            name='hands_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_hands',
                to='base.handsslotitem',
                verbose_name='Предмет на кисти',
            ),
        ),
        migrations.AddField(
            model_name='npc',
            name='head_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_heads',
                to='base.headslotitem',
                verbose_name='Предмет на голову',
            ),
        ),
        migrations.AddField(
            model_name='npc',
            name='left_ring_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_left_rings',
                to='base.ringsslotitem',
                verbose_name='Кольцо на левую руку',
            ),
        ),
        migrations.AddField(
            model_name='npc',
            name='right_ring_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_right_rings',
                to='base.ringsslotitem',
                verbose_name='Кольцо на правую руку',
            ),
        ),
        migrations.AddField(
            model_name='npc',
            name='waist_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_waists',
                to='base.waistslotitem',
                verbose_name='Предмет на пояс',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='neck_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_necks',
                to='base.neckslotitem',
                verbose_name='Предмет на шею',
            ),
        ),
    ]