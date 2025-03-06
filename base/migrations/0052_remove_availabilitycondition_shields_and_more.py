from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0051_auto_20250305_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilitycondition',
            name='shields',
        ),
        migrations.RemoveField(
            model_name='class',
            name='shields',
        ),
        migrations.RemoveField(
            model_name='subclass',
            name='shields',
        ),
    ]
