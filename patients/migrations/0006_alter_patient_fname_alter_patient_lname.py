# Generated by Django 5.0.6 on 2024-05-27 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_patient_password_alter_patient_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='fname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='lname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
