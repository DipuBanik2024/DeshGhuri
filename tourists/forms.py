from django import forms
from .models import Tourist

class TouristProfileForm(forms.ModelForm):
    class Meta:
        model = Tourist
        fields = [
            'phone_number',
            'date_of_birth',
            'bio',
            'profile_picture',
            'address',
            'travel_style',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
