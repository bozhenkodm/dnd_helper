# Generated by Django 4.0.2 on 2022-02-12 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0005_delete_armsslotitem_armsslotitem2_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HandsSlotItem',
            new_name='ArmsSlotItem',
        ),
        migrations.DeleteModel(
            name='ArmsSlotItem2',
        ),
        migrations.CreateModel(
            name='HandsSlotItem',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('base.simplemagicitem',),
        ),
        migrations.AlterField(
            model_name='npc',
            name='arms_slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='npc_arms',
                to='base.handsslotitem',
                verbose_name='Arms slot',
            ),
        ),
    ]
