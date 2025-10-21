from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import GuideProfile, TourRequest, Tour, Earning, Review
from tourists.models import Tourist
from .forms import GuideProfileForm, TourRequestForm, ReviewForm
from accounts.utils import role_required
from django.contrib.auth import get_user_model
from django.template.defaulttags import register
from django.utils import timezone
from django.db.models import Sum
from datetime import date

# Import Notification model from hotels app
from hotels.models import Notification

User = get_user_model()


# Add template filters at the top (after imports)
@register.filter
def split(value, key):
    """Split string by delimiter"""
    return value.split(key) if value else []


@register.filter
def strip(value):
    """Strip whitespace from string"""
    return value.strip() if value else ''


# --------------------------
# HELPER FUNCTIONS
# --------------------------
def update_guide_rating(guide_user):
    """Update guide's average rating based on all reviews"""
    reviews = Review.objects.filter(guide=guide_user)
    if reviews.count() > 0:
        avg_rating = sum(review.rating for review in reviews) / reviews.count()
        guide_profile = GuideProfile.objects.get(user=guide_user)
        guide_profile.average_rating = round(avg_rating, 2)
        guide_profile.save()


# --------------------------
# PUBLIC GUIDE LIST (Tourist view)
# --------------------------
def guide_list(request):
    guides = GuideProfile.objects.select_related("user").filter(is_completed=True)

    # Calculate stats for the template
    verified_guides_count = guides.filter(is_verified=True).count()

    # Calculate average experience
    total_experience = sum(guide.experience_years for guide in guides)
    avg_experience = round(total_experience / len(guides)) if guides else 0

    # Count unique languages
    all_languages = set()
    for guide in guides:
        if guide.languages:
            languages = [lang.strip() for lang in guide.languages.split(',')]
            all_languages.update(languages)
    total_languages = len(all_languages)

    context = {
        'guides': guides,
        'verified_guides_count': verified_guides_count,
        'avg_experience': avg_experience,
        'total_languages': total_languages,
    }

    return render(request, "guides/guide_list.html", context)


# --------------------------
# GUIDE DASHBOARD
# --------------------------
@login_required
@role_required(['guide'])
def guide_dashboard(request):
    profile, created = GuideProfile.objects.get_or_create(user=request.user)

    # Today's tours
    today_tours_count = Tour.objects.filter(
        guide=request.user,
        start_date=date.today()
    ).count()

    # Pending requests
    pending_requests_count = TourRequest.objects.filter(
        guide=request.user,
        status="pending"
    ).count()

    # Monthly earnings (current month)
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_earnings = Earning.objects.filter(
        guide=request.user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Recent requests (last 5)
    recent_requests = TourRequest.objects.filter(
        guide=request.user,
        status="pending"
    ).order_by('-created_at')[:3]

    # Recent reviews (last 3)
    recent_reviews = Review.objects.filter(
        guide=request.user
    ).select_related('tourist').order_by('-created_at')[:3]

    # Review count
    review_count = Review.objects.filter(guide=request.user).count()

    # UNREAD NOTIFICATIONS COUNT - ADDED FOR NOTIFICATION SYSTEM
    unread_notifications_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    context = {
        'profile': profile,
        'today_tours_count': today_tours_count,
        'pending_requests_count': pending_requests_count,
        'monthly_earnings': monthly_earnings,
        'recent_requests': recent_requests,
        'recent_reviews': recent_reviews,
        'review_count': review_count,
        'unread_notifications_count': unread_notifications_count,  # ADDED FOR NOTIFICATION SYSTEM
    }

    return render(request, "guides/guide_dashboard.html", context)


# --------------------------
# GUIDE NOTIFICATION VIEWS
# --------------------------
@login_required
@role_required(['guide'])
def mark_guide_notifications_read(request):
    """Mark all notifications as read for guide"""
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read!")
    return redirect('guide_dashboard')


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
            guide_profile.refresh_from_db()
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
        profile.refresh_from_db()
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

    # CREATE NOTIFICATION FOR TOURIST - ADDED FOR NOTIFICATION SYSTEM
    Notification.objects.create(
        user=tr.tourist,
        message=f"Your tour request for {tr.destination} has been accepted by {request.user.get_full_name()}",
    )

    messages.success(request, "Tour request accepted successfully!")
    return redirect('tour_requests')


@login_required
@role_required(['guide'])
def reject_request(request, request_id):
    tr = get_object_or_404(TourRequest, id=request_id, guide=request.user)
    tr.status = "rejected"
    tr.save()

    # CREATE NOTIFICATION FOR TOURIST - ADDED FOR NOTIFICATION SYSTEM
    Notification.objects.create(
        user=tr.tourist,
        message=f"Your tour request for {tr.destination} has been declined by {request.user.get_full_name()}",
    )

    messages.success(request, "Tour request rejected.")
    return redirect('tour_requests')


# --------------------------
# MY TOURS & TOUR DETAILS
# --------------------------
@login_required
@role_required(['guide'])
def my_tours(request):
    tours = Tour.objects.filter(guide=request.user)
    return render(request, "guides/my_tours.html", {"tours": tours})


@login_required
@role_required(['guide'])
def tour_detail(request, tour_id):
    # Get the tour object or return 404
    tour = get_object_or_404(Tour, id=tour_id, guide=request.user)

    # Get guide profile with contact information
    guide_profile = None
    try:
        guide_profile = GuideProfile.objects.get(user=tour.guide)
    except GuideProfile.DoesNotExist:
        pass

    # Get tourist profiles for all tourists in this tour
    tourist_profiles = []
    for tourist_user in tour.tourists.all():
        try:
            tourist_profile = Tourist.objects.get(user=tourist_user)
            tourist_profiles.append({
                'user': tourist_user,
                'profile': tourist_profile
            })
        except Tourist.DoesNotExist:
            tourist_profiles.append({
                'user': tourist_user,
                'profile': None
            })

    context = {
        'tour': tour,
        'guide_profile': guide_profile,
        'tourist_profiles': tourist_profiles,
    }
    return render(request, "guides/tour_detail.html", context)


# --------------------------
# EARNINGS
# --------------------------
@login_required
@role_required(['guide'])
def earnings(request):
    earnings = Earning.objects.filter(guide=request.user).order_by('-date')
    total = sum(e.amount for e in earnings)

    # Calculate completed tours count - FIXED
    completed_tours_count = Tour.objects.filter(
        guide=request.user,
        status="completed"
    ).count()

    # Alternative: Count from earnings if tours aren't marked as completed
    if completed_tours_count == 0:
        completed_tours_count = earnings.count()

    # Calculate average earnings per tour - FIXED
    avg_per_tour = 0
    if completed_tours_count > 0:
        avg_per_tour = round(total / completed_tours_count, 2)
    else:
        avg_per_tour = total  # If no completed tours but has earnings

    # Get monthly earnings
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_earnings = Earning.objects.filter(
        guide=request.user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # For chart max value
    max_amount = max([e.amount for e in earnings]) if earnings else 0

    context = {
        'earnings': earnings,
        'total': total,
        'monthly_earnings': monthly_earnings,
        'completed_tours_count': completed_tours_count,
        'avg_per_tour': avg_per_tour,
        'max_amount': max_amount,
    }
    return render(request, "guides/earnings.html", context)


# --------------------------
# MESSAGES
# --------------------------
@login_required
@role_required(['guide'])
def guide_messages(request):
    return render(request, "guides/messages.html")


# --------------------------
# REVIEW MANAGEMENT VIEWS
# --------------------------

# CREATE REVIEW
@login_required
@role_required(['tourist'])
def create_review(request, guide_id):
    guide_user = get_object_or_404(User, id=guide_id)
    guide_profile = get_object_or_404(GuideProfile, user=guide_user)

    # Check if user already reviewed this guide
    existing_review = Review.objects.filter(guide=guide_user, tourist=request.user).first()
    if existing_review:
        messages.info(request, "You have already reviewed this guide. You can edit your existing review.")
        return redirect('edit_review', review_id=existing_review.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.guide = guide_user
            review.tourist = request.user
            review.save()

            # CREATE NOTIFICATION FOR GUIDE - ADDED FOR NOTIFICATION SYSTEM
            Notification.objects.create(
                user=guide_user,
                message=f"New {review.rating}-star review from {request.user.get_full_name()}",
            )

            # Update guide's average rating
            update_guide_rating(guide_user)

            messages.success(request, "Review submitted successfully!")
            return redirect("guide_detail", guide_id=guide_profile.id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'guide': guide_profile,
        'action': 'Create'
    }
    return render(request, "guides/review_form.html", context)


# EDIT REVIEW
@login_required
@role_required(['tourist'])
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, tourist=request.user)
    guide_profile = get_object_or_404(GuideProfile, user=review.guide)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()

            # Update guide's average rating
            update_guide_rating(review.guide)

            messages.success(request, "Review updated successfully!")
            return redirect("guide_detail", guide_id=guide_profile.id)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'guide': guide_profile,
        'review': review,
        'action': 'Edit'
    }
    return render(request, "guides/review_form.html", context)


# DELETE REVIEW
@login_required
@role_required(['tourist'])
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, tourist=request.user)
    guide_profile = get_object_or_404(GuideProfile, user=review.guide)

    if request.method == "POST":
        review.delete()

        # Update guide's average rating
        update_guide_rating(review.guide)

        messages.success(request, "Review deleted successfully!")
        return redirect("guide_detail", guide_id=guide_profile.id)

    context = {
        'review': review,
        'guide': guide_profile
    }
    return render(request, "guides/confirm_delete_review.html", context)


# --------------------------
# PUBLIC GUIDE DETAIL (Tourist view) - UPDATED VERSION
# --------------------------
def guide_detail(request, guide_id):
    guide = get_object_or_404(GuideProfile, id=guide_id)

    # Get reviews and calculate stats
    reviews = Review.objects.filter(guide=guide.user).select_related('tourist').order_by('-created_at')
    review_count = reviews.count()

    # Calculate average rating
    if review_count > 0:
        avg_rating = sum(review.rating for review in reviews) / review_count
        guide.average_rating = round(avg_rating, 2)
        guide.save()

    # Handle booking form
    booking_form = None
    if request.user.is_authenticated and getattr(request.user, "role", None) == "tourist":
        if request.method == "POST" and 'submit_booking' in request.POST:
            booking_form = TourRequestForm(request.POST)
            if booking_form.is_valid():
                tour_request = booking_form.save(commit=False)
                tour_request.tourist = request.user
                tour_request.guide = guide.user
                tour_request.save()

                # CREATE NOTIFICATION FOR GUIDE - ADDED FOR NOTIFICATION SYSTEM
                Notification.objects.create(
                    user=guide.user,
                    message=f"New tour request from {request.user.get_full_name()} for {tour_request.destination}",
                )

                messages.success(request, "Tour request sent successfully!")
                return redirect("guide_detail", guide_id=guide.id)
        else:
            booking_form = TourRequestForm()

    # Handle review form - SIMPLIFIED VERSION
    user_review = None
    review_form = None
    if request.user.is_authenticated and getattr(request.user, "role", None) == "tourist":
        user_review = Review.objects.filter(guide=guide.user, tourist=request.user).first()

        # Initialize form for template context
        review_form = ReviewForm(instance=user_review) if user_review else ReviewForm()

    # Calculate additional stats for template
    completed_tours = Tour.objects.filter(guide=guide.user, status="completed").count()

    # Count languages
    total_languages = 0
    if guide.languages:
        languages = [lang.strip() for lang in guide.languages.split(',')]
        total_languages = len(languages)

    context = {
        'guide': guide,
        'form': booking_form,  # Keep for backward compatibility
        'booking_form': booking_form,
        'reviews': reviews,
        'review_count': review_count,
        'completed_tours': completed_tours,
        'total_languages': total_languages,
        'user_review': user_review,
        'review_form': review_form,  # Add this for template context
    }

    return render(request, "guides/guide_detail.html", context)


@login_required
@role_required(['tourist'])
def book_guide(request, guide_id):
    guide = get_object_or_404(GuideProfile, id=guide_id)

    if request.method == "POST":
        form = TourRequestForm(request.POST)
        if form.is_valid():
            tour_request = form.save(commit=False)
            tour_request.tourist = request.user
            tour_request.guide = guide.user
            tour_request.save()

            # CREATE NOTIFICATION FOR GUIDE - ADDED FOR NOTIFICATION SYSTEM
            Notification.objects.create(
                user=guide.user,
                message=f"New tour request from {request.user.get_full_name()} for {tour_request.destination}",
            )

            messages.success(request, "Tour request sent successfully!")
            return redirect("guide_detail", guide_id=guide.id)
    else:
        # Pre-fill destination with guide's location or a default
        initial_data = {'destination': guide.address or 'Explore with guide'}
        form = TourRequestForm(initial=initial_data)

    context = {
        'guide': guide,
        'form': form,
    }
    return render(request, "guides/book_guide.html", context)