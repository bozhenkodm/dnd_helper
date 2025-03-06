from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_remove_itemstate_shield'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemstate',
            old_name='shield_m2m',
            new_name='shield',
        ),
    ]
