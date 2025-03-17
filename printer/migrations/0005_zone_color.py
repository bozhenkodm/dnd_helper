# Generated by Django 5.1.7 on 2025-03-17 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0004_alter_zone_map_alter_zone_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='color',
            field=models.CharField(
                choices=[
                    ('none', 'Пусто'),
                    ('white', 'Белый'),
                    ('green', 'Зелёный'),
                    ('red', 'Красный'),
                    ('black', 'Чёрный'),
                ],
                max_length=20,
                null=True,
                verbose_name='Color',
            ),
        ),
    ]
