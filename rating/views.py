from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from .forms import RatingForm
from .models import Rating
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from math import floor


def average_star_rating(current_rating, star_rating, counter):
    rating = floor(((current_rating * counter) + star_rating) / (counter + 1))
    return rating


def RateDoctor(request, doctor_id):
    """Handles Patient rating a Docotr."""
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            doctor = Doctor.objects.get(pk=doctor_id)
            patient = Patient.objects.get(user=request.user)
            # Check appointment history before allowing rating
            
            has_appointment_history = Appointment.objects.filter(
                doctor=doctor,
                patient=patient,
            ).exists()

            if has_appointment_history:

                existing_rating = Rating.objects.filter(
                    rater_patient=patient,
                    rated_doctor = doctor,
                ).first()

                if existing_rating:
                    # Update existing rating
                    score = form.cleaned_data['score']
                    existing_rating.score = score
                    existing_rating.review = form.cleaned_data['review']
                    
                    doctor.rating = average_star_rating(doctor.rating, score, doctor.rating_counter)
                    doctor.save()
                    existing_rating.save()
                    messages.success(request, "Rating Updated Successfully!")
                    return redirect('BrowseDoctors')
                else:
                    # Create new rating
                    ratings = form.save(commit=False)
                    ratings.rated_doctor = Doctor.objects.get(pk=doctor_id)
                    score = form.cleaned_data['score']
                    ratings.review = form.cleaned_data['review']
                    ratings.rater_patient = patient

                    rated = average_star_rating(doctor.rating, form.cleaned_data['score'], doctor.rating_counter)
                    doctor.rating = rated
                    doctor.rating_counter = doctor.rating_counter + 1
                    doctor.save()


                    ratings.ratings = rated
                    ratings.save()
                    messages.success(request, "Doctor Rated Successfully!")
                    return redirect('BrowseDoctors')
                               

            else:
                messages.error(request, "You can only rate doctors with whom you've had appointment with.")
                return redirect('BrowseDoctors')  

        else:
            messages.error(request, "Invalid Review")
    else:
        doctor = Doctor.objects.get(pk=doctor_id)
        patient = Patient.objects.get(user=request.user)

        # Check for existing rating and prepopulate form
        existing_rating = Rating.objects.filter(
              rater_patient=patient,
              rated_doctor = doctor,
        ).first()

        if existing_rating:
            form = RatingForm(initial={'score': existing_rating.score, 'review': existing_rating.review, 'doctor': doctor})
        else:
            form = RatingForm(initial={'doctor': doctor})

        context = {
            'tenant': doctor,
            'form': form,
        }
    return render(request, 'rating/rating.html', context)

