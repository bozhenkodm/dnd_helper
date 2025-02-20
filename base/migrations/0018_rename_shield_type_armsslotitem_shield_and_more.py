# Generated by Django 5.1.6 on 2025-02-20 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_armsslotitem_unique_together_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='armsslotitem',
            old_name='shield_type',
            new_name='shield',
        ),
        migrations.AlterUniqueTogether(
            name='armsslotitem',
            unique_together={('magic_item_type', 'level', 'shield')},
        ),
    ]
