# Generated by Django 3.2.9 on 2021-11-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0036_alter_npc_trained_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.SmallIntegerField(
                choices=[
                    (10, 'Апостол'),
                    (20, 'Артефактор'),
                    (30, 'Бард'),
                    (35, 'Вампир'),
                    (40, 'Варвар'),
                    (50, 'Военачальник'),
                    (60, 'Воин'),
                    (70, 'Волшебник'),
                    (80, 'Друид'),
                    (90, 'Жрец'),
                    (95, 'Ловчий'),
                    (100, 'Каратель'),
                    (110, 'Колдун'),
                    (120, 'Мечник-маг'),
                    (125, 'Монах'),
                    (130, 'Паладин'),
                    (140, 'Плут'),
                    (150, 'Рунный жрец'),
                    (160, 'Следопыт (Дальнобойный)'),
                    (170, 'Следопыт (Рукопашник)'),
                    (175, 'Хексблэйд (колдун)'),
                    (180, 'Хранитель'),
                    (190, 'Чародей'),
                    (200, 'Шаман'),
                ],
                unique=True,
                verbose_name='Название',
            ),
        ),
    ]
