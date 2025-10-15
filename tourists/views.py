from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Tourist
from .forms import TouristProfileForm
from accounts.utils import role_required
from guides.models import TourRequest  # ✅ ADD THIS
from packages.models import Booking  # ✅ ADD THIS


# --------------------------
# TOURIST DASHBOARD (ENHANCED)
# --------------------------
@login_required
@role_required(['tourist'])
def tourist_dashboard(request):
    profile, created = Tourist.objects.get_or_create(user=request.user)

    # Get all guide bookings for this tourist
    guide_bookings = TourRequest.objects.filter(
        tourist=request.user
    ).select_related('guide', 'guide__guideprofile').order_by('-created_at')

    # Get all package bookings for this tourist
    package_bookings = Booking.objects.filter(
        tourist=request.user
    ).select_related('package').order_by('-booking_date')

    # Calculate stats
    total_guide_bookings = guide_bookings.count()
    total_package_bookings = package_bookings.count()
    pending_guide_requests = guide_bookings.filter(status='pending').count()
    accepted_guide_requests = guide_bookings.filter(status='accepted').count()

    context = {
        'profile': profile,
        'guide_bookings': guide_bookings,
        'package_bookings': package_bookings,
        'total_guide_bookings': total_guide_bookings,
        'total_package_bookings': total_package_bookings,
        'pending_guide_requests': pending_guide_requests,
        'accepted_guide_requests': accepted_guide_requests,
    }
    return render(request, "tourists/dashboard.html", context)


# --------------------------
# TOURIST HOME (Keep existing)
# --------------------------
@login_required
@role_required(['tourist'])
def tourist_home(request):
    profile, created = Tourist.objects.get_or_create(user=request.user)
    return render(request, "tourists/tourist_home.html", {"profile": profile})


# --------------------------
# TOURIST PROFILE VIEW (Keep existing)
# --------------------------
@login_required
@role_required(['tourist'])
def tourist_profile(request):
    profile = get_object_or_404(Tourist, user=request.user)
    return render(request, "tourists/profile.html", {"profile": profile})


# --------------------------
# EDIT TOURIST PROFILE (Keep existing)
# --------------------------
@login_required
@role_required(['tourist'])
def edit_tourist_profile(request):
    profile, created = Tourist.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = TouristProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('tourist_profile')
    else:
        form = TouristProfileForm(instance=profile)

    return render(request, "tourists/edit_profile.html", {"form": form})


def create_tour_requests(request):
    # Your create tour request logic here
    return render(request, 'tourists/create_tour_request.html')