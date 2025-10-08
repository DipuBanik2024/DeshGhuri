from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import GuideProfile, TourRequest, Tour, Earning
from .forms import GuideProfileForm, TourRequestForm
from accounts.utils import role_required
from django.contrib.auth import get_user_model

User = get_user_model()


# --------------------------
# GUIDE DASHBOARD
# --------------------------
@login_required
@role_required(['guide'])
def guide_dashboard(request):
    profile, created = GuideProfile.objects.get_or_create(user=request.user)
    bookings = getattr(request.user, 'booking_set', None)
    bookings = bookings.all() if bookings else []
    return render(request, "guides/guide_dashboard.html", {"profile": profile, "bookings": bookings})


# --------------------------
# EDIT GUIDE PROFILE
# --------------------------
@login_required
@role_required(['guide'])
def edit_guide_profile(request):
    profile, created = GuideProfile.objects.get_or_create(user=request.user)

    if profile.user != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = GuideProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            guide_profile = form.save(commit=False)
            guide_profile.is_completed = True
            guide_profile.save()
            guide_profile.refresh_from_db()  # ✅ force reload from DB
            messages.success(request, "Profile updated successfully!")
            return redirect('guide_profile')
    else:
        form = GuideProfileForm(instance=profile)

    return render(request, "guides/edit_profile.html", {"form": form})


# --------------------------
# GUIDE PROFILE VIEW
# --------------------------
@login_required
@role_required(['guide'])
def guide_profile(request):
    profile = GuideProfile.objects.filter(user=request.user).first()
    if profile:
        profile.refresh_from_db()  # ✅ ensures fresh data every time
    return render(request, "guides/profile.html", {"guide_profile": profile})


# --------------------------
# TOUR REQUESTS (Guide view)
# --------------------------
@login_required
@role_required(['guide'])
def tour_requests(request):
    requests = TourRequest.objects.filter(guide=request.user, status="pending")
    return render(request, "guides/tour_requests.html", {"requests": requests})


@login_required
@role_required(['guide'])
def accept_request(request, request_id):
    tr = get_object_or_404(TourRequest, id=request_id, guide=request.user)
    tr.status = "accepted"
    tr.save()

    # Tour creation
    tour = Tour.objects.create(
        guide=request.user,
        destination=tr.destination,
        start_date=tr.date,
        end_date=tr.date,
        price=tr.price if tr.price else 0.00
    )
    tour.tourists.add(tr.tourist)
    tour.save()

    # Add earning
    if tr.price:
        Earning.objects.create(
            guide=request.user,
            amount=tr.price,
            description=f"Tour to {tr.destination}"
        )

    messages.success(request, "Tour request accepted successfully!")
    return redirect('tour_requests')


@login_required
@role_required(['guide'])
def reject_request(request, request_id):
    tr = get_object_or_404(TourRequest, id=request_id, guide=request.user)
    tr.status = "rejected"
    tr.save()
    messages.success(request, "Tour request rejected.")
    return redirect('tour_requests')


# --------------------------
# MY TOURS
# --------------------------
@login_required
@role_required(['guide'])
def my_tours(request):
    tours = Tour.objects.filter(guide=request.user)
    return render(request, "guides/my_tours.html", {"tours": tours})


# --------------------------
# EARNINGS
# --------------------------
@login_required
@role_required(['guide'])
def earnings(request):
    earnings = Earning.objects.filter(guide=request.user)
    total = sum(e.amount for e in earnings)
    return render(request, "guides/earnings.html", {"earnings": earnings, "total": total})


# --------------------------
# MESSAGES
# --------------------------
@login_required
@role_required(['guide'])
def guide_messages(request):
    return render(request, "guides/messages.html")


# --------------------------
# PUBLIC GUIDE LIST (Tourist view)
# --------------------------
def guide_list(request):
    guides = GuideProfile.objects.select_related("user").all()
    return render(request, "guides/guide_list.html", {"guides": guides})


# --------------------------
# PUBLIC GUIDE DETAIL (Tourist view)
# --------------------------
def guide_detail(request, guide_id):
    guide = get_object_or_404(GuideProfile, id=guide_id)

    # Tourist booking
    if request.user.is_authenticated and getattr(request.user, "role", None) == "tourist":
        if request.method == "POST":
            form = TourRequestForm(request.POST)
            if form.is_valid():
                tour_request = form.save(commit=False)
                tour_request.tourist = request.user
                tour_request.guide = guide.user
                tour_request.save()
                messages.success(request, "Tour request sent successfully!")
                return redirect("guide_detail", guide_id=guide.id)
        else:
            form = TourRequestForm()
    else:
        form = None

    return render(request, "guides/guide_detail.html", {"guide": guide, "form": form})
