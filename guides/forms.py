from django import forms
from .models import GuideProfile

class GuideProfileForm(forms.ModelForm):
    class Meta:
        model = GuideProfile
        fields = ["phone","bio","experience_years"]

