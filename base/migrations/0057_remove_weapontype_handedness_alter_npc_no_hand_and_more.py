import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0056_auto_20250306_0754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weapontype',
            name='handedness',
        ),
        migrations.AlterField(
            model_name='npc',
            name='no_hand',
            field=models.ForeignKey(
                blank=True,
                help_text="Armament that doesn't take hand slot",
                limit_choices_to={'weapon_type__handedness_fk__name': 'FREE'},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='in_no_hands',
                to='base.weapon',
                verbose_name='No hand implement',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='primary_hand',
            field=models.ForeignKey(
                blank=True,
                limit_choices_to=models.Q(
                    ('weapon_type__handedness_fk__name', 'FREE'), _negated=True
                ),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='in_primary_hands',
                to='base.weapon',
                verbose_name='Primary hand',
            ),
        ),
        migrations.AlterField(
            model_name='npc',
            name='secondary_hand',
            field=models.ForeignKey(
                blank=True,
                limit_choices_to=models.Q(
                    ('weapon_type__handedness_fk__name', 'FREE'), _negated=True
                ),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='in_secondary_hands',
                to='base.weapon',
                verbose_name='Secondary hand',
            ),
        ),
    ]
