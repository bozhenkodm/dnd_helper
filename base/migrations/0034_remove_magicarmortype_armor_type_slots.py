from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_auto_20250305_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magicarmortype',
            name='armor_type_slots',
        ),
    ]
