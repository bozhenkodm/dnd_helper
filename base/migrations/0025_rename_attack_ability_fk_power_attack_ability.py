from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_remove_power_attack_ability'),
    ]

    operations = [
        migrations.RenameField(
            model_name='power',
            old_name='attack_ability_fk',
            new_name='attack_ability',
        ),
    ]
