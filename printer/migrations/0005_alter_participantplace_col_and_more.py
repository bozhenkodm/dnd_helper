# Generated by Django 5.1.4 on 2025-01-02 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0004_alter_participantplace_col_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantplace',
            name='col',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='participantplace',
            name='row',
            field=models.SmallIntegerField(default=0),
        ),
    ]