from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_magicweapontype_implement_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='magicweapontype',
            name='weapon_categories_m2m',
            field=models.ManyToManyField(
                blank=True, to='base.weaponcategory', verbose_name='Weapon category'
            ),
        ),
    ]
