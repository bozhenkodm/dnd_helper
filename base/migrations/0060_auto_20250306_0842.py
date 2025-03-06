from django.db import migrations


def fill_data(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0059_alter_weaponhandedness_name'),
    ]

    operations = [migrations.RunPython(fill_data)]
