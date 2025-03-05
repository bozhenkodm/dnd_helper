import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_remove_availabilitycondition_weapon_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magicweapontype',
            name='implement_type',
            field=models.ForeignKey(
                blank=True,
                help_text='Does item has additional implement property?',
                limit_choices_to={'category__code': 7},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='base.weapontype',
                verbose_name='Implement type',
            ),
        ),
    ]
