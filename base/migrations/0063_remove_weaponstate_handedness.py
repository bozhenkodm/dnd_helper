from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0062_auto_20250306_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weaponstate',
            name='handedness',
        ),
    ]
