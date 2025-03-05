from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_auto_20250305_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='power',
            name='attack_ability',
        ),
    ]
