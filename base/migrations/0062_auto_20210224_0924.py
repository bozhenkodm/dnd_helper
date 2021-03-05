# Generated by Django 3.1.3 on 2021-02-24 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0061_auto_20210224_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='power',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активный/Пассивный'),
        ),
        migrations.AlterField(
            model_name='power',
            name='action_type',
            field=models.CharField(
                choices=[
                    ('STANDARD', 'Стандартное действие'),
                    ('MINOR', 'Малое действие'),
                    ('FREE', 'Свободное действие'),
                    ('MOVEMENT', 'Действие движения'),
                    ('PROVOKED', 'Провоцированное действие'),
                    ('INTERRUPT', 'Немедленное прерывание'),
                    ('REACTION', 'Немедленный ответ'),
                    ('NO_ACTION', 'Нет действия'),
                ],
                default='STANDARD',
                max_length=9,
                null=True,
                verbose_name='Действие',
            ),
        ),
        migrations.AlterField(
            model_name='power',
            name='range_type',
            field=models.CharField(
                choices=[
                    ('MELEE_WEAPON', 'Рукопашное оружие'),
                    ('MELEE_DISTANCE', 'Рукопашное (дистанция)'),
                    ('MELEE_TOUCH', 'Рукопашное касание'),
                    ('MELEE_RANGED_WEAPON', 'Рукопашное или дальнобойное оружие'),
                    ('PERSONAL', 'Персональный'),
                    ('RANGED_WEAPON', 'Дальнобойное оружие'),
                    ('RANGED_DISTANCE', 'Дальнобойное (дистанция)'),
                    ('RANGED_SIGHT', 'Дальнобойное (видимость)'),
                    ('CLOSE_BURST', 'Ближняя вспышка'),
                    ('CLOSE_BLAST', 'Ближняя волна'),
                    ('AREA_BURST', 'Зональная вспышка'),
                    ('AREA_WALL', 'Стена'),
                ],
                default='PERSONAL',
                max_length=19,
                verbose_name='Дальность',
            ),
        ),
    ]
