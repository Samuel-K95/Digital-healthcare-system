# Generated by Django 5.0.6 on 2024-06-19 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0009_alter_doctor_city'),
        ('patients', '0009_remove_patient_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined'), ('rescheduled', 'Rescheduled'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to='doctors.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointments', to='patients.patient')),
            ],
        ),
    ]
