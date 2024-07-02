from doctors.models import Doctor
from patients.models import Patient


def get_role(user):
    if user is None:
        return 'anonymous'
    if user.is_superuser or user.is_staff:
        return 'admin'
    if Doctor.objects.filter(user=user).exists():
        return 'doctor'
    if Patient.objects.filter(user=user).exists():
        return 'patient'
    return 'user'


def can_create_appointment(user, doctor, patient):
    role = get_role(user)
    if role == 'admin':
        return True
    if role == 'patient' and patient and getattr(patient, 'user', None) == user:
        return True
    if role == 'doctor' and doctor and getattr(doctor, 'user', None) == user:
        return True
    # Allow anonymous for backward compatibility only if explicitly desired (not recommended)
    return False


def can_view_appointment(user, appointment):
    role = get_role(user)
    if role == 'admin':
        return True
    if role == 'doctor' and appointment.doctor and appointment.doctor.user == user:
        return True
    if role == 'patient' and appointment.patient and appointment.patient.user == user:
        return True
    return False


def can_edit_appointment(user, appointment):
    # Only allow editing if allowed by policies: patient editing own pending, doctor editing own
    role = get_role(user)
    if role == 'admin':
        return True
    if role == 'doctor' and appointment.doctor and appointment.doctor.user == user:
        return True
    if role == 'patient' and appointment.patient and appointment.patient.user == user and appointment.status == 'pending':
        return True
    return False


def can_delete_appointment(user, appointment):
    # Similar rules to edit
    return can_edit_appointment(user, appointment)
