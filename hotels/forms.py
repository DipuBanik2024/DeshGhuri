from django import forms
from .models import Hotel, RoomType, HotelBooking, HotelReview, HotelImage


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'name', 'address', 'phone', 'description', 'profile_image',
            'city', 'area', 'landmark',
            'has_wifi', 'has_pool', 'has_ac', 'has_breakfast',
            'has_parking', 'has_gym'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = [
            'name', 'description', 'capacity', 'price_per_night', 'available_rooms', 'room_image',
            'has_ac', 'has_tv', 'has_balcony', 'room_size'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ['image', 'caption']


class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = [
            'check_in', 'check_out', 'number_of_rooms', 'total_guests',
            'guest_name', 'guest_email', 'guest_phone', 'special_requests'
        ]
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }


class HotelSearchForm(forms.Form):
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City or Area'}))
    check_in = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    guests = forms.IntegerField(required=False, min_value=1, initial=1)
    rooms = forms.IntegerField(required=False, min_value=1, initial=1)

    # Filter options
    min_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2)

    RATING_CHOICES = [
        ('', 'Any Rating'),
        ('4.5', '4.5+ Stars'),
        ('4.0', '4.0+ Stars'),
        ('3.5', '3.5+ Stars'),
        ('3.0', '3.0+ Stars'),
    ]
    min_rating = forms.ChoiceField(required=False, choices=RATING_CHOICES)

    # Amenities
    amenities = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('wifi', 'Free WiFi'),
            ('pool', 'Swimming Pool'),
            ('ac', 'Air Conditioning'),
            ('breakfast', 'Breakfast Included'),
            ('parking', 'Free Parking'),
            ('gym', 'Gym'),
        ],
        widget=forms.CheckboxSelectMultiple
    )


class HotelReviewForm(forms.ModelForm):
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
        model = HotelReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Share your experience with this hotel... How was your stay? Any suggestions?'
            }),
        }
        labels = {
            'comment': 'Your Review'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].required = True
        # Note: comment is not required since model allows blank=True