from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0049_rename_shield_m2m_itemstate_shield'),
    ]

    operations = [
        migrations.AddField(
            model_name='availabilitycondition',
            name='shields_m2m',
            field=models.ManyToManyField(
                blank=True, to='base.shieldtype', verbose_name='Available shields'
            ),
        ),
        migrations.AddField(
            model_name='class',
            name='shields_m2m',
            field=models.ManyToManyField(
                blank=True, to='base.shieldtype', verbose_name='Available shields'
            ),
        ),
        migrations.AddField(
            model_name='subclass',
            name='shields_m2m',
            field=models.ManyToManyField(
                blank=True, to='base.shieldtype', verbose_name='Available shields'
            ),
        ),
    ]
