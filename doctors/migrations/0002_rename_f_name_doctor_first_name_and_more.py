# Generated by Django 5.0.6 on 2024-06-18 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='f_name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='doctor',
            old_name='l_name',
            new_name='last_name',
        ),
    ]
