from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_rename_category_m2m_weaponstate_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='availabilitycondition',
            name='weapon_categories_m2m',
            field=models.ManyToManyField(
                blank=True,
                to='base.weaponcategory',
                verbose_name='Available weapon categories',
            ),
        ),
        migrations.AddField(
            model_name='class',
            name='weapon_categories_m2m',
            field=models.ManyToManyField(
                blank=True,
                to='base.weaponcategory',
                verbose_name='Available weapon categories',
            ),
        ),
        migrations.AddField(
            model_name='subclass',
            name='weapon_categories_m2m',
            field=models.ManyToManyField(
                blank=True,
                to='base.weaponcategory',
                verbose_name='Available weapon categories',
            ),
        ),
    ]
