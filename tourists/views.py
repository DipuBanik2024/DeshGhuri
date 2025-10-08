from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Tourist
from .forms import TouristProfileForm
from accounts.utils import role_required

# --------------------------
# TOURIST DASHBOARD
# --------------------------
@login_required
@role_required(['tourist'])
def tourist_dashboard(request):
    profile, created = Tourist.objects.get_or_create(user=request.user)
    return render(request, "tourist/tourist_dashboard.html", {"profile": profile})

# --------------------------
# TOURIST PROFILE VIEW
# --------------------------
@login_required
@role_required(['tourist'])
def tourist_profile(request):
    profile = get_object_or_404(Tourist, user=request.user)
    return render(request, "tourists/profile.html", {"profile": profile})

# --------------------------
# EDIT TOURIST PROFILE
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

