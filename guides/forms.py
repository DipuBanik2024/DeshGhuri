from django import forms
from .models import GuideProfile, TourRequest


class GuideProfileForm(forms.ModelForm):
    class Meta:
        model = GuideProfile
        # Future-proof: include all optional fields
        fields = ["phone", "bio", "experience_years", "languages", "address" , "avatar"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone number"}),
            "bio": forms.Textarea(attrs={"placeholder": "Write a short bio"}),
            "experience_years": forms.NumberInput(attrs={"min": 0}),
            "languages": forms.TextInput(attrs={"placeholder": "Languages you speak"}),

            "address": forms.Textarea(attrs={"placeholder": "Your address"}),
        }


class TourRequestForm(forms.ModelForm):
    class Meta:
        model = TourRequest
        fields = ['destination', 'date', 'price', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter destination'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter proposed price',
                'step': '0.01',
                'min': '0'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Any special requirements...'
            }),
        }
        labels = {
            'price': 'Proposed Price (BDT)',
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price