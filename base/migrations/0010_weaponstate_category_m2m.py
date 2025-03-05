from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_rename_category_fk_weapontype_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='weaponstate',
            name='category_m2m',
            field=models.ManyToManyField(
                blank=True, to='base.weaponcategory', verbose_name='Weapon category'
            ),
        ),
    ]
