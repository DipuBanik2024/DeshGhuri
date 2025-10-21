from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Q, Avg, Count
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .models import Hotel, RoomType, HotelBooking, HotelReview, Notification, HotelImage
from .forms import HotelForm, RoomTypeForm, HotelBookingForm, HotelSearchForm, HotelReviewForm, HotelImageForm
from accounts.utils import role_required
from datetime import datetime, timedelta


@login_required
@role_required(['hotel_manager'])
def hotel_dashboard(request):
    hotels = Hotel.objects.filter(owner=request.user)

    # Get bookings for all hotels owned by this user
    bookings = HotelBooking.objects.filter(hotel__owner=request.user).select_related('tourist', 'room_type').order_by(
        '-created_at')

    # Statistics
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='pending').count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    today_checkins = bookings.filter(check_in=timezone.now().date(), status='confirmed').count()

    # Recent bookings (last 7 days)
    recent_bookings = bookings.filter(created_at__gte=timezone.now() - timedelta(days=7))

    context = {
        'hotels': hotels,
        'bookings': bookings[:10],  # Last 10 bookings
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'today_checkins': today_checkins,
        'recent_bookings_count': recent_bookings.count(),
    }
    return render(request, "hotels/hotel_dashboard.html", context)


@login_required
@role_required(['hotel_manager'])
def hotel_create(request):
    if request.method == "POST":
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            messages.success(request, "Hotel created successfully!")
            return redirect('hotel_dashboard')
    else:
        form = HotelForm()
    return render(request, "hotels/hotel_form.html", {"form": form})


@login_required
@role_required(['hotel_manager'])
def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if hotel.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel updated successfully!")
            return redirect('hotel_dashboard')
    else:
        form = HotelForm(instance=hotel)
    return render(request, "hotels/hotel_form.html", {"form": form})


@login_required
@role_required(['hotel_manager'])
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if hotel.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        hotel.delete()
        messages.success(request, "Hotel deleted successfully!")
        return redirect('hotel_dashboard')
    return render(request, "hotels/hotel_confirm_delete.html", {"hotel": hotel})


@login_required
@role_required(['hotel_manager'])
def manage_rooms(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id, owner=request.user)
    room_types = hotel.room_types.all()

    if request.method == "POST":
        form = RoomTypeForm(request.POST, request.FILES)
        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.hotel = hotel
            room_type.save()
            hotel.update_price_range()
            messages.success(request, "Room type added successfully!")
            return redirect('manage_rooms', hotel_id=hotel_id)
    else:
        form = RoomTypeForm()

    context = {
        'hotel': hotel,
        'room_types': room_types,
        'form': form,
    }
    return render(request, "hotels/manage_rooms.html", context)


@login_required
@role_required(['hotel_manager'])
def room_type_edit(request, hotel_id, room_type_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id, owner=request.user)
    room_type = get_object_or_404(RoomType, pk=room_type_id, hotel=hotel)

    if request.method == "POST":
        form = RoomTypeForm(request.POST, request.FILES, instance=room_type)
        if form.is_valid():
            form.save()
            hotel.update_price_range()
            messages.success(request, "Room type updated successfully!")
            return redirect('manage_rooms', hotel_id=hotel_id)
    else:
        form = RoomTypeForm(instance=room_type)

    context = {
        'hotel': hotel,
        'room_type': room_type,
        'form': form,
    }
    return render(request, "hotels/room_type_form.html", context)


@login_required
@role_required(['hotel_manager'])
def room_type_delete(request, hotel_id, room_type_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id, owner=request.user)
    room_type = get_object_or_404(RoomType, pk=room_type_id, hotel=hotel)

    if request.method == "POST":
        room_type.delete()
        hotel.update_price_range()
        messages.success(request, "Room type deleted successfully!")
        return redirect('manage_rooms', hotel_id=hotel_id)

    context = {
        'hotel': hotel,
        'room_type': room_type,
    }
    return render(request, "hotels/room_type_confirm_delete.html", context)


@login_required
@role_required(['hotel_manager'])
def manage_hotel_images(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id, owner=request.user)
    gallery_images = hotel.gallery_images.all()

    if request.method == "POST":
        form = HotelImageForm(request.POST, request.FILES)
        if form.is_valid():
            hotel_image = form.save(commit=False)
            hotel_image.hotel = hotel
            hotel_image.save()
            messages.success(request, "Image added successfully!")
            return redirect('manage_hotel_images', hotel_id=hotel_id)
    else:
        form = HotelImageForm()

    context = {
        'hotel': hotel,
        'gallery_images': gallery_images,
        'form': form,
    }
    return render(request, "hotels/manage_hotel_images.html", context)


@login_required
@role_required(['hotel_manager'])
def delete_hotel_image(request, hotel_id, image_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id, owner=request.user)
    hotel_image = get_object_or_404(HotelImage, pk=image_id, hotel=hotel)

    if request.method == "POST":
        hotel_image.delete()
        messages.success(request, "Image deleted successfully!")

    return redirect('manage_hotel_images', hotel_id=hotel_id)


@login_required
@role_required(['hotel_manager'])
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(HotelBooking, pk=booking_id, hotel__owner=request.user)

    if status in ['confirmed', 'cancelled', 'completed']:
        booking.status = status
        booking.save()

        # Create notification for tourist
        Notification.objects.create(
            user=booking.tourist,
            message=f"Your booking at {booking.hotel.name} has been {status}.",
            booking=booking
        )

        messages.success(request, f"Booking {status} successfully!")

    return redirect('hotel_dashboard')


# Public views
def hotels_info(request):
    form = HotelSearchForm(request.GET or None)
    hotels = Hotel.objects.all().annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )

    if form.is_valid():
        location = form.cleaned_data.get('location')
        min_rating = form.cleaned_data.get('min_rating')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        amenities = form.cleaned_data.get('amenities', [])

        # Location filter
        if location:
            hotels = hotels.filter(
                Q(city__icontains=location) |
                Q(area__icontains=location) |
                Q(landmark__icontains=location) |
                Q(address__icontains=location)
            )

        # Rating filter
        if min_rating:
            hotels = hotels.filter(avg_rating__gte=float(min_rating))

        # Price filter
        if min_price:
            hotels = hotels.filter(min_price__gte=min_price)
        if max_price:
            hotels = hotels.filter(max_price__lte=max_price)

        # Amenities filter
        amenity_filters = Q()
        if 'wifi' in amenities:
            amenity_filters |= Q(has_wifi=True)
        if 'pool' in amenities:
            amenity_filters |= Q(has_pool=True)
        if 'ac' in amenities:
            amenity_filters |= Q(has_ac=True)
        if 'breakfast' in amenities:
            amenity_filters |= Q(has_breakfast=True)
        if 'parking' in amenities:
            amenity_filters |= Q(has_parking=True)
        if 'gym' in amenities:
            amenity_filters |= Q(has_gym=True)

        if amenities:
            hotels = hotels.filter(amenity_filters)

    context = {
        'hotels': hotels,
        'form': form,
    }
    return render(request, "hotels/hotels_list.html", context)


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room_types = hotel.room_types.all()
    reviews = hotel.reviews.all().select_related('tourist').order_by('-created_at')
    gallery_images = hotel.gallery_images.all()

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'hotel': hotel,
        'room_types': room_types,
        'reviews': reviews,
        'gallery_images': gallery_images,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
    }
    return render(request, "hotels/hotel_detail.html", context)


@login_required
@role_required(['tourist'])
def book_hotel(request, hotel_id, room_type_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room_type = get_object_or_404(RoomType, pk=room_type_id, hotel=hotel)

    # Check room availability
    if room_type.available_rooms <= 0:
        messages.error(request, "Sorry, this room type is currently unavailable.")
        return redirect('hotel_detail', hotel_id=hotel_id)

    if request.method == "POST":
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tourist = request.user
            booking.hotel = hotel
            booking.room_type = room_type
            booking.room_price = room_type.price_per_night

            # Calculate total amount
            nights = (booking.check_out - booking.check_in).days
            if nights <= 0:
                messages.error(request, "Check-out date must be after check-in date.")
                return render(request, "hotels/hotel_booking.html", {
                    'hotel': hotel,
                    'room_type': room_type,
                    'form': form
                })

            booking.total_amount = room_type.price_per_night * booking.number_of_rooms * nights

            # Check if requested rooms are available
            if booking.number_of_rooms > room_type.available_rooms:
                messages.error(request, f"Only {room_type.available_rooms} rooms available for this type.")
                return render(request, "hotels/hotel_booking.html", {
                    'hotel': hotel,
                    'room_type': room_type,
                    'form': form
                })

            booking.save()

            # Create notifications
            Notification.objects.create(
                user=request.user,
                message=f"Your booking at {hotel.name} is pending confirmation.",
                booking=booking
            )
            Notification.objects.create(
                user=hotel.owner,
                message=f"New booking request for {hotel.name} from {request.user.get_full_name()}.",
                booking=booking
            )

            messages.success(request, "Hotel booking request submitted successfully!")
            return redirect('tourist_dashboard')
    else:
        # Pre-fill guest information from user profile
        initial_data = {
            'guest_name': request.user.get_full_name(),
            'guest_email': request.user.email,
            'guest_phone': getattr(request.user.tourist_profile, 'phone_number', ''),
        }
        form = HotelBookingForm(initial=initial_data)

    context = {
        'hotel': hotel,
        'room_type': room_type,
        'form': form,
    }
    return render(request, "hotels/hotel_booking.html", context)


@login_required
def submit_review(request, booking_id):
    booking = get_object_or_404(HotelBooking, pk=booking_id, tourist=request.user)

    # Check if booking is completed
    if booking.status != 'completed':
        messages.error(request, "You can only review completed bookings.")
        return redirect('tourist_dashboard')

    # Check if already reviewed
    if HotelReview.objects.filter(booking=booking, tourist=request.user).exists():
        messages.error(request, "You have already reviewed this booking.")
        return redirect('tourist_dashboard')

    if request.method == "POST":
        form = HotelReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = booking.hotel
            review.tourist = request.user
            review.booking = booking
            review.save()

            # Update hotel average rating
            hotel = booking.hotel
            hotel_reviews = hotel.reviews.all()
            if hotel_reviews:
                avg_rating = hotel_reviews.aggregate(Avg('rating'))['rating__avg']
                hotel.average_rating = round(avg_rating, 2)
                hotel.save()

            messages.success(request, "Thank you for your review!")
            return redirect('tourist_dashboard')
    else:
        form = HotelReviewForm()

    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, "hotels/submit_review.html", context)


# Direct hotel review (without booking requirement)
@login_required
@role_required(['tourist'])
def submit_hotel_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)

    # Check if user already reviewed this hotel
    existing_review = HotelReview.objects.filter(hotel=hotel, tourist=request.user).first()
    if existing_review:
        messages.info(request, "You have already reviewed this hotel. You can edit your existing review.")
        return redirect('edit_review', review_id=existing_review.id)

    if request.method == "POST":
        form = HotelReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = hotel
            review.tourist = request.user
            # No booking required for direct reviews
            review.save()

            # Update hotel average rating
            hotel_reviews = hotel.reviews.all()
            if hotel_reviews:
                avg_rating = hotel_reviews.aggregate(Avg('rating'))['rating__avg']
                hotel.average_rating = round(avg_rating, 2)
                hotel.save()

            messages.success(request, "Thank you for your review!")
            return redirect('hotel_detail', hotel_id=hotel_id)
    else:
        form = HotelReviewForm()

    context = {
        'hotel': hotel,
        'form': form,
        'review_type': 'create'
    }
    return render(request, "hotels/submit_review.html", context)


# Edit review view
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(HotelReview, pk=review_id, tourist=request.user)

    if request.method == "POST":
        form = HotelReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.save()  # This will update updated_at field

            # Update hotel average rating
            hotel = review.hotel
            hotel_reviews = hotel.reviews.all()
            if hotel_reviews:
                avg_rating = hotel_reviews.aggregate(Avg('rating'))['rating__avg']
                hotel.average_rating = round(avg_rating, 2)
                hotel.save()

            messages.success(request, "Review updated successfully!")
            return redirect('hotel_detail', hotel_id=review.hotel.id)
    else:
        form = HotelReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
        'hotel': review.hotel,
        'review_type': 'edit'
    }
    return render(request, "hotels/submit_review.html", context)


# Delete review view
@login_required
@require_http_methods(["POST"])
def delete_review(request, review_id):
    review = get_object_or_404(HotelReview, pk=review_id, tourist=request.user)
    hotel_id = review.hotel.id
    review.delete()

    # Update hotel average rating
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    hotel_reviews = hotel.reviews.all()
    if hotel_reviews:
        avg_rating = hotel_reviews.aggregate(Avg('rating'))['rating__avg']
        hotel.average_rating = round(avg_rating, 2) if avg_rating else 0.00
    else:
        hotel.average_rating = 0.00
    hotel.save()

    messages.success(request, "Review deleted successfully!")
    return redirect('hotel_detail', hotel_id=hotel_id)


# My reviews view
@login_required
def my_reviews(request):
    reviews = HotelReview.objects.filter(tourist=request.user).select_related('hotel').order_by('-created_at')

    context = {
        'reviews': reviews
    }
    return render(request, "hotels/my_reviews.html", context)


@login_required
@role_required(['hotel_manager'])
def booking_detail(request, booking_id):
    """Hotel manager can view booking details"""
    booking = get_object_or_404(HotelBooking, pk=booking_id, hotel__owner=request.user)
    return render(request, "hotels/booking_detail.html", {"booking": booking})


@login_required
def my_notifications(request):
    """View all notifications for the current user"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "tourists/notifications.html", {"notifications": notifications})


@login_required
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    messages.success(request, "Notification marked as read!")
    return redirect('my_notifications')


def hotel_search_api(request):
    """API endpoint for hotel search (for AJAX requests)"""
    if request.method == "GET":
        location = request.GET.get('location', '')
        min_rating = request.GET.get('min_rating', '')

        hotels = Hotel.objects.all().annotate(
            avg_rating=Avg('reviews__rating')
        )

        if location:
            hotels = hotels.filter(
                Q(city__icontains=location) |
                Q(area__icontains=location) |
                Q(name__icontains=location)
            )

        if min_rating:
            hotels = hotels.filter(avg_rating__gte=float(min_rating))

        hotel_data = []
        for hotel in hotels[:10]:  # Limit to 10 results
            hotel_data.append({
                'id': hotel.id,
                'name': hotel.name,
                'city': hotel.city,
                'area': hotel.area,
                'min_price': float(hotel.min_price),
                'avg_rating': float(hotel.avg_rating) if hotel.avg_rating else 0.0,
            })

        return JsonResponse({'hotels': hotel_data})


@login_required
@role_required(['hotel_manager'])
def mark_hotel_notifications_read(request):
    """Mark all notifications as read for hotel manager"""
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read!")
    return redirect('hotel_dashboard')