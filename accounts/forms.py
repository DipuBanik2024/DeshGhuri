from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    agree_terms = forms.BooleanField(
        required=True,
        label='I agree to the Terms & Conditions'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "password1",
            "password2",
              # ✅ new field added
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'h-4 w-4 text-cyan-500 border-gray-300 rounded'
            elif field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = (
                    'w-full px-4 py-2 border rounded-md focus:outline-none '
                    'focus:ring-2 focus:ring-cyan-400'
                )
            else:
                field.widget.attrs['class'] = (
                    'w-full px-4 py-2 border rounded-md focus:outline-none '
                    'focus:ring-2 focus:ring-cyan-400'
                )

    # optional: friendly unique username check
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    # ✅ ensure terms must be accepted
