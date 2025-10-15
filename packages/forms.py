from django import forms
from .models import Booking
from django.utils import timezone
import datetime


class PackageBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['people_count', 'tour_date', 'mobile_number']
        widgets = {
            'tour_date': forms.DateInput(attrs={'type': 'date'}),
            'people_count': forms.NumberInput(attrs={'min': 1, 'max': 20}),
            'mobile_number': forms.TextInput(),
        }

    def clean_tour_date(self):
        tour_date = self.cleaned_data.get('tour_date')
        if tour_date and tour_date < timezone.now().date():
            raise forms.ValidationError("Tour date cannot be in the past!")
        return tour_date

    def clean_people_count(self):
        people_count = self.cleaned_data.get('people_count')
        if people_count and people_count < 1:
            raise forms.ValidationError("Number of people must be at least 1!")
        return people_count

    # 🔥 CRITICAL: Add this mobile number validation that your view expects!
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number:
            raise forms.ValidationError("Mobile number is required!")
        return mobile_number