from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'review']
        widgets = {
            'score': forms.RadioSelect(choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars'))),
            'review': forms.Textarea(attrs={'placeholder': 'Write a review (optional)'}),
        }
