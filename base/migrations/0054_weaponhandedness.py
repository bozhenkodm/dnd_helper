from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0053_rename_shields_m2m_availabilitycondition_shields_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeaponHandedness',
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
                    models.CharField(
                        choices=[
                            ('OFF_HAND', 'Дополнительное'),
                            ('ONE', 'Одноручное'),
                            ('VERSATILE', 'Универсальное'),
                            ('TWO', 'Двуручное'),
                            ('FREE', 'Не занимает руки'),
                        ],
                        max_length=9,
                        verbose_name='Handedness',
                    ),
                ),
                (
                    'is_one_handed',
                    models.BooleanField(
                        default=True, null=True, verbose_name='One handed'
                    ),
                ),
            ],
        ),
    ]
