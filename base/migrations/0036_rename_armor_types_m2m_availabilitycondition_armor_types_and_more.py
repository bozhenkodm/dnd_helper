from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_remove_availabilitycondition_armor_types_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availabilitycondition',
            old_name='armor_types_m2m',
            new_name='armor_types',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='armor_types_m2m',
            new_name='armor_types',
        ),
        migrations.RenameField(
            model_name='magicarmortype',
            old_name='armor_type_slots_m2m',
            new_name='armor_type_slots',
        ),
        migrations.RenameField(
            model_name='subclass',
            old_name='armor_types_m2m',
            new_name='armor_types',
        ),
    ]
