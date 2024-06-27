from django.db import models
from doctors.models import Doctor
from patients.models import Patient

class Rating(models.Model):
    #rater
    rated_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , related_name="rated_doctor")
    #rated entity
    rater_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    #rating detail
    score = models.IntegerField()
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rater_patient} rated {self.rated_doctor}  - {self.score} Stars"
