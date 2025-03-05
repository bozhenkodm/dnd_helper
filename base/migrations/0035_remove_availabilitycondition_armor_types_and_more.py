from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_remove_magicarmortype_armor_type_slots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilitycondition',
            name='armor_types',
        ),
        migrations.RemoveField(
            model_name='class',
            name='armor_types',
        ),
        migrations.RemoveField(
            model_name='subclass',
            name='armor_types',
        ),
    ]
