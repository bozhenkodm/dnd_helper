from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0040_rename_base_armor_type_fk_armortype_base_armor_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='magicarmitemtype',
            name='shield_slots_m2m',
            field=models.ManyToManyField(
                blank=True, to='base.shieldtype', verbose_name='Shield slots'
            ),
        ),
    ]
