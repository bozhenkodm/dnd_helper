from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20250305_0617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilitycondition',
            name='weapon_categories',
        ),
        migrations.RemoveField(
            model_name='class',
            name='weapon_categories',
        ),
        migrations.RemoveField(
            model_name='subclass',
            name='weapon_categories',
        ),
    ]
