# Generated by Django 4.0.2 on 2022-02-15 15:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0016_classskill_class_trainable_skills_classskill_klass_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AbilityModel',
            new_name='Ability',
        ),
        migrations.RenameModel(
            old_name='SkillModel',
            new_name='Skill',
        ),
    ]
