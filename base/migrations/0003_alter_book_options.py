# Generated by Django 5.1.4 on 2025-02-13 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_book_booksource'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
    ]
