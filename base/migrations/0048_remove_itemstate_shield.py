from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_auto_20250305_2158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemstate',
            name='shield',
        ),
    ]
