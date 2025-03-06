from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0063_remove_weaponstate_handedness'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weaponstate',
            old_name='handedness_m2m',
            new_name='handedness',
        ),
    ]
