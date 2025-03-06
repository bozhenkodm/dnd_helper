from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0052_remove_availabilitycondition_shields_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availabilitycondition',
            old_name='shields_m2m',
            new_name='shields',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='shields_m2m',
            new_name='shields',
        ),
        migrations.RenameField(
            model_name='subclass',
            old_name='shields_m2m',
            new_name='shields',
        ),
    ]
