# Generated by Django 3.2.4 on 2021-06-09 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salecars', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auto',
            old_name='model_id',
            new_name='model',
        ),
        migrations.RenameField(
            model_name='auto',
            old_name='region_id',
            new_name='region',
        ),
        migrations.RenameField(
            model_name='models',
            old_name='model_id',
            new_name='model',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='city_id',
            new_name='city',
        ),
    ]
