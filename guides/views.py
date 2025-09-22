from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import GuideProfile
from .forms import GuideProfileForm
from accounts.utils import role_required

@login_required
@role_required(['guide'])
def guide_dashboard(request):
    profile = get_object_or_404(GuideProfile, user=request.user)
    # Bookings can be accessed via related_name in Booking model if needed
    bookings = request.user.booking_set.all()  # Assuming Booking model has guide field pointing to GuideProfile
    return render(request, "guides/dashboard.html", {"profile": profile, "bookings": bookings})

@login_required
@role_required(['guide'])
def edit_guide_profile(request):
    profile, created = GuideProfile.objects.get_or_create(user=request.user)
    if profile.user != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method == "POST":
        form = GuideProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect('guide_dashboard')
    else:
        form = GuideProfileForm(instance=profile)
    return render(request, "guides/edit_profile.html", {"form": form})
def guides_info(request):
    guides = Guide.objects.all()
    return render(request, "guides/info.html", {"guides": guides})
