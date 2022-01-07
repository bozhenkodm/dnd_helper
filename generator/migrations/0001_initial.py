# Generated by Django 4.0 on 2022-01-07 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPCName',
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
                    'name',
                    models.CharField(max_length=30, unique=True, verbose_name='Имя'),
                ),
                (
                    'name_type',
                    models.CharField(
                        choices=[('first', 'Имя'), ('last', 'Фамилия')],
                        max_length=10,
                        verbose_name='Тип',
                    ),
                ),
                (
                    'sex',
                    models.CharField(
                        blank=True,
                        choices=[('M', 'Муж'), ('F', 'Жен'), ('N', 'Н/Д')],
                        max_length=1,
                        null=True,
                        verbose_name='Пол',
                    ),
                ),
                ('race', models.ManyToManyField(to='base.Race')),
            ],
            options={
                'verbose_name': 'Имя',
                'verbose_name_plural': 'Имена',
            },
        ),
    ]
