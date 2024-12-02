# Generated by Django 5.1.3 on 2024-12-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0044_alter_weapontype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magicitemtype',
            name='slot',
            field=models.CharField(
                choices=[
                    ('ARMOR', 'Броня'),
                    ('HEAD', 'Голова'),
                    ('RING', 'Кольца'),
                    ('FEET', 'Обувь'),
                    ('WEAPON', 'Оружие'),
                    ('HANDS', 'Перчатки'),
                    ('WAIST', 'Пояс'),
                    ('ARMS', 'Предплечья/Щит'),
                    ('TATOO', 'Татуировка'),
                    ('WONDROUS_ITEMS', 'Чудесный предмет'),
                    ('NECK', 'Шея'),
                ],
                max_length=14,
                null=True,
                verbose_name='Slot',
            ),
        ),
    ]
