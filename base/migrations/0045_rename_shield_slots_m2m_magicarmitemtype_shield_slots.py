from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0044_remove_magicarmitemtype_shield_slots'),
    ]

    operations = [
        migrations.RenameField(
            model_name='magicarmitemtype',
            old_name='shield_slots_m2m',
            new_name='shield_slots',
        ),
    ]
