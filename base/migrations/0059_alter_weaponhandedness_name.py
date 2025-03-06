from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_rename_handedness_fk_weapontype_handedness_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weaponhandedness',
            name='name',
            field=models.CharField(
                choices=[
                    ('OFF_HAND', 'Дополнительное'),
                    ('ONE', 'Одноручное'),
                    ('VERSATILE', 'Универсальное'),
                    ('TWO', 'Двуручное'),
                    ('FREE', 'Не занимает руки'),
                ],
                max_length=9,
                unique=True,
                verbose_name='Handedness',
            ),
        ),
    ]
