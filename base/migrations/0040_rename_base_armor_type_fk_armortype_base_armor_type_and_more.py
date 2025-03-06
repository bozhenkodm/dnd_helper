from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_remove_armortype_base_armor_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='armortype',
            old_name='base_armor_type_fk',
            new_name='base_armor_type',
        ),
        migrations.RenameField(
            model_name='itemstate',
            old_name='armor_m2m',
            new_name='armor',
        ),
    ]
