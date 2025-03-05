import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_rename_attack_ability_fk_power_attack_ability'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseArmorType',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'armor_class',
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, 'Тканевый'),
                            (2, 'Кожаный'),
                            (3, 'Шкурный'),
                            (6, 'Кольчуга'),
                            (7, 'Чешуйчатый'),
                            (8, 'Латный'),
                        ],
                        verbose_name='Name',
                    ),
                ),
                (
                    'is_light',
                    models.BooleanField(default=True, verbose_name='Is light?'),
                ),
                (
                    'speed_penalty',
                    models.SmallIntegerField(default=0, verbose_name='Speed penalty'),
                ),
                (
                    'skill_penalty',
                    models.SmallIntegerField(default=0, verbose_name='Skills penalty'),
                ),
            ],
        ),
        migrations.AddField(
            model_name='armortype',
            name='base_armor_type_fk',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='base.basearmortype',
                verbose_name='Armor type',
            ),
        ),
    ]
