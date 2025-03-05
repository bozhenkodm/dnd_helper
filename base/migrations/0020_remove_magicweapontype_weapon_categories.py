from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20250305_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magicweapontype',
            name='weapon_categories',
        ),
    ]
