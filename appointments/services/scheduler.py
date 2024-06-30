from datetime import datetime, timedelta, time
from django.utils import timezone
from appointments.models import Appointment


def detect_conflict(doctor, start_dt: datetime, end_dt: datetime):
    """Return True if any appointment for doctor overlaps [start_dt, end_dt)."""
    conflicts = Appointment.objects.filter(doctor=doctor, appointment_date__lt=end_dt, appointment_date__gte=start_dt)
    return conflicts.exists()


def find_available_slots(doctor, start_dt: datetime, end_dt: datetime, duration_minutes: int = 30, buffer_minutes: int = 0):
    """Naive slot generator: iterate windows between start_dt and end_dt and return slots that have no conflicts.

    This implementation assumes appointments are point-starts and uses duration to check for overlapping appointments.
    """
    slots = []
    slot_length = timedelta(minutes=duration_minutes + buffer_minutes)
    cursor = start_dt
    while cursor + timedelta(minutes=duration_minutes) <= end_dt:
        slot_start = cursor
        slot_end = cursor + timedelta(minutes=duration_minutes)
        if not detect_conflict(doctor, slot_start, slot_end):
            slots.append({'start': slot_start, 'end': slot_end})
        cursor += timedelta(minutes=duration_minutes)
    return slots


def book_slot_atomic(doctor, patient, slot_start: datetime, duration_minutes: int = 30):
    """Attempt to book a slot atomically. Returns created Appointment or raises an exception on conflict."""
    # Simple optimistic approach: re-check conflicts and create
    slot_end = slot_start + timedelta(minutes=duration_minutes)
    if detect_conflict(doctor, slot_start, slot_end):
        raise ValueError('Slot conflict')
    appt = Appointment.objects.create(doctor=doctor, patient=patient, appointment_date=slot_start)
    return appt
