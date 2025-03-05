from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20250304_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weaponstate',
            name='category',
        ),
    ]
