from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0060_auto_20250306_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='weaponstate',
            name='handedness_m2m',
            field=models.ManyToManyField(
                blank=True, to='base.weaponhandedness', verbose_name='Handedness'
            ),
        ),
    ]
