import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            'base',
            '0021_rename_weapon_categories_m2m_availabilitycondition_weapon_categories_and_more',
        ),
    ]

    operations = [
        migrations.AddField(
            model_name='power',
            name='attack_ability_fk',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='base.ability',
                verbose_name='Attack ability',
            ),
        ),
    ]
