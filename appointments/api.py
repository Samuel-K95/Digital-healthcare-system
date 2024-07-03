from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import json

from doctors.models import Doctor
from patients.models import Patient
from .services.scheduler import find_available_slots, book_slot_atomic
from access.policy import can_create_appointment



@require_GET
def available_slots(request, doctor_id):
    start = request.GET.get('start')
    end = request.GET.get('end')
    duration = int(request.GET.get('duration', '30'))
    if not start or not end:
        return JsonResponse({'error': 'start and end query params required'}, status=400)
    # URL encoding may convert '+' in ISO offsets to spaces; normalize back
    start = start.replace(' ', '+')
    end = end.replace(' ', '+')
    start_dt = parse_datetime(start)
    end_dt = parse_datetime(end)
    if start_dt is None or end_dt is None:
        return JsonResponse({'error': 'invalid datetime format'}, status=400)
    doctor = Doctor.objects.filter(id=doctor_id).first()
    if not doctor:
        return JsonResponse({'error': 'doctor not found'}, status=404)
    slots = find_available_slots(doctor, start_dt, end_dt, duration_minutes=duration)
    out = [{'start': s['start'].isoformat(), 'end': s['end'].isoformat()} for s in slots]
    return JsonResponse({'slots': out})


@csrf_exempt
@require_POST
def create_appointment(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid json'}, status=400)
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')
    slot_start = data.get('slot_start')
    duration = int(data.get('duration', 30))
    if not doctor_id or not patient_id or not slot_start:
        return JsonResponse({'error': 'doctor_id, patient_id, and slot_start are required'}, status=400)
    doctor = Doctor.objects.filter(id=doctor_id).first()
    if not doctor:
        return JsonResponse({'error': 'doctor not found'}, status=404)
    patient = Patient.objects.filter(id=patient_id).first()
    if not patient:
        return JsonResponse({'error': 'patient not found'}, status=404)
    # Enforce policy: require authenticated user to create appointments
    if not request.user or not request.user.is_authenticated:
        return JsonResponse({'error': 'authentication required'}, status=401)
    if not can_create_appointment(request.user, doctor, patient):
        return JsonResponse({'error': 'forbidden'}, status=403)
    slot_dt = parse_datetime(slot_start.replace(' ', '+'))
    if slot_dt is None:
        return JsonResponse({'error': 'invalid slot_start datetime'}, status=400)
    try:
        appt = book_slot_atomic(doctor, patient, slot_dt, duration_minutes=duration)
    except ValueError:
        return JsonResponse({'error': 'slot conflict'}, status=409)
    return JsonResponse({'appointment_id': appt.id})
