from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_weapontype_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weapontype',
            old_name='category_fk',
            new_name='category',
        ),
    ]
