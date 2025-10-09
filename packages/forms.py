from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['people_count', 'tour_date', 'mobile_number']  # mobile_number add করা
        widgets = {
            'tour_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'people_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +8801234567890'}),
        }
