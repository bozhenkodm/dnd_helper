from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_weaponcategory_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weapontype',
            name='category',
        ),
    ]
