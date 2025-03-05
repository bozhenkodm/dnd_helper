from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_rename_shield_slots_m2m_magicarmitemtype_shield_slots'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemstate',
            name='shield_m2m',
            field=models.ManyToManyField(
                blank=True, to='base.shieldtype', verbose_name='Shield type'
            ),
        ),
    ]
