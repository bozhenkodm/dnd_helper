import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0054_weaponhandedness'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapontype',
            name='handedness_fk',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='base.weaponhandedness',
                verbose_name='Handedness',
            ),
        ),
        migrations.AlterField(
            model_name='armortype',
            name='base_armor_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='base.basearmortype',
                verbose_name='Armor type',
            ),
        ),
        migrations.AlterField(
            model_name='weapontype',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='base.weaponcategory',
                verbose_name='Category',
            ),
        ),
    ]
