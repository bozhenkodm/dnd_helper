from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_auto_20250305_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='magicarmortype',
            name='armor_type_slots_m2m',
            field=models.ManyToManyField(
                to='base.basearmortype', verbose_name='Armor type slots'
            ),
        ),
    ]
