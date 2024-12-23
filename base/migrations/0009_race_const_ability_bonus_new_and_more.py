# Generated by Django 5.1.4 on 2024-12-23 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_rename_based_on_new_skill_based_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='const_ability_bonus_new',
            field=models.ManyToManyField(
                related_name='races_with_const_ability',
                to='base.ability',
                verbose_name='Constant ability bonuses',
            ),
        ),
        migrations.AddField(
            model_name='race',
            name='var_ability_bonus_new',
            field=models.ManyToManyField(
                related_name='races',
                to='base.ability',
                verbose_name='Selective ability bonus',
            ),
        ),
        migrations.AlterField(
            model_name='race',
            name='var_ability_bonus',
            field=models.ManyToManyField(
                to='base.ability', verbose_name='Selective ability bonus'
            ),
        ),
    ]
