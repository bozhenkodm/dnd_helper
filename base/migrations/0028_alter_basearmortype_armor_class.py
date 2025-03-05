from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_auto_20250305_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basearmortype',
            name='armor_class',
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, 'Тканевый'),
                    (2, 'Кожаный'),
                    (3, 'Шкурный'),
                    (6, 'Кольчуга'),
                    (7, 'Чешуйчатый'),
                    (8, 'Латный'),
                ],
                unique=True,
                verbose_name='Name',
            ),
        ),
    ]
