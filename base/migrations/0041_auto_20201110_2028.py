# Generated by Django 3.1.3 on 2020-11-10 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0040_auto_20201110_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racebonus',
            name='image',
            field=models.ImageField(
                blank=True, null=True, upload_to='images/', verbose_name='Картинка'
            ),
        ),
    ]
