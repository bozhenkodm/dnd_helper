from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0043_auto_20250305_2135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magicarmitemtype',
            name='shield_slots',
        ),
    ]
