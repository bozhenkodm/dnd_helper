# Generated by Django 5.1.4 on 2024-12-23 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_race_const_ability_bonus_new_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='const_ability_bonus_new',
            field=models.ManyToManyField(
                related_name='races_with_const_ability',
                to='base.abilitynew',
                verbose_name='Constant ability bonuses',
            ),
        ),
        migrations.AlterField(
            model_name='race',
            name='var_ability_bonus_new',
            field=models.ManyToManyField(
                related_name='races',
                to='base.abilitynew',
                verbose_name='Selective ability bonus',
            ),
        ),
    ]