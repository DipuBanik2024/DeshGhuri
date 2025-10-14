from django import forms
from .models import GuideProfile, TourRequest, Review


class GuideProfileForm(forms.ModelForm):
    class Meta:
        model = GuideProfile
        fields = ["phone", "bio", "experience_years", "languages", "address", "avatar"]
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
        fields = ['destination', 'date', 'number_of_travelers', 'duration_hours', 'places_to_explore', 'price', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter destination'
            }),
            'number_of_travelers': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Number of people',
                'min': '1',
                'max': '20'
            }),
            'duration_hours': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'places_to_explore': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Specific places you want to visit...'
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
                'placeholder': 'Any special requirements, dietary restrictions, or additional notes...'
            }),
        }
        labels = {
            'price': 'Proposed Price (BDT)',
            'number_of_travelers': 'Number of Travelers',
            'duration_hours': 'Tour Duration',
            'places_to_explore': 'Places to Explore',
        }

    def __init__(self, *args, **kwargs):
        self.guide_destination = kwargs.pop('guide_destination', None)
        super().__init__(*args, **kwargs)

        if self.guide_destination:
            self.fields['places_to_explore'].widget.attrs[
                'placeholder'] = f'What to explore in {self.guide_destination}? e.g., Tea Gardens, Ratargul...'

        self.fields['duration_hours'].choices = [
            ('', 'Select duration'),
            (2, '2 hours (Quick tour)'),
            (4, '4 hours (Half day)'),
            (8, '8 hours (Full day)'),
            (12, '12 hours (Full day+)'),
        ]

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price


# ENHANCED ReviewForm with proper rating widget
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label='Your Rating'
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Share your experience with this guide... What did you like? Any suggestions?'
            }),
        }
        labels = {
            'comment': 'Your Review'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make rating field required
        self.fields['rating'].required = True
        self.fields['comment'].required = True