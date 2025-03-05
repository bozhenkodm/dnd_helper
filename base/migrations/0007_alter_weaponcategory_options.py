from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20250303_2046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weaponcategory',
            options={
                'verbose_name': 'Weapon category',
                'verbose_name_plural': 'Weapon categories',
            },
        ),
    ]
