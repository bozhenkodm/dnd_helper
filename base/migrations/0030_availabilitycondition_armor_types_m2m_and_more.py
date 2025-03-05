from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_auto_20250305_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='availabilitycondition',
            name='armor_types_m2m',
            field=models.ManyToManyField(
                blank=True,
                to='base.basearmortype',
                verbose_name='Available armor types',
            ),
        ),
        migrations.AddField(
            model_name='class',
            name='armor_types_m2m',
            field=models.ManyToManyField(
                blank=True,
                to='base.basearmortype',
                verbose_name='Available armor types',
            ),
        ),
        migrations.AddField(
            model_name='subclass',
            name='armor_types_m2m',
            field=models.ManyToManyField(
                blank=True,
                to='base.basearmortype',
                verbose_name='Available armor types',
            ),
        ),
    ]
