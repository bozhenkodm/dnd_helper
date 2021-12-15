# Generated by Django 4.0 on 2021-12-13 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_armor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='magicitem',
            name='category',
            field=models.CharField(
                choices=[
                    ('COMMON', 'Обычный'),
                    ('UNCOMMON', 'Необычный'),
                    ('RARE', 'Редкий'),
                ],
                default='COMMON',
                max_length=8,
                verbose_name='Категория',
            ),
        ),
    ]