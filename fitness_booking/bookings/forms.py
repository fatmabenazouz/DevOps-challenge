from django import forms
from .models import Booking

class BookingFeedbackForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['feedback', 'rating']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }