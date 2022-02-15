# Generated by Django 4.0.2 on 2022-02-15 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_class_trainable_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='var_ability_bonus',
            field=models.ManyToManyField(
                related_name='races',
                to='base.Ability',
                verbose_name='Выборочные бонусы характеристик',
            ),
        ),
    ]
