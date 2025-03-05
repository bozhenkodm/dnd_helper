from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_remove_weaponstate_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weaponstate',
            old_name='category_m2m',
            new_name='categories',
        ),
    ]
