from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_remove_magicweapontype_weapon_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availabilitycondition',
            old_name='weapon_categories_m2m',
            new_name='weapon_categories',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='weapon_categories_m2m',
            new_name='weapon_categories',
        ),
        migrations.RenameField(
            model_name='magicweapontype',
            old_name='weapon_categories_m2m',
            new_name='weapon_categories',
        ),
        migrations.RenameField(
            model_name='subclass',
            old_name='weapon_categories_m2m',
            new_name='weapon_categories',
        ),
    ]
