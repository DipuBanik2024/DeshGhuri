from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Hotel
from .forms import HotelForm
from accounts.utils import role_required

@login_required
@role_required(['hotel_manager'])
def hotel_dashboard(request):
    hotels = Hotel.objects.filter(owner=request.user)
    # Bookings can be accessed via related_name in Booking model if needed
    bookings = request.user.booking_set.all()  # Assuming Booking model has hotel field pointing to Hotel
    return render(request, "hotels/hotel_dashboard.html", {"hotels": hotels, "bookings": bookings})

@login_required
@role_required(['hotel_manager'])
def hotel_create(request):
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            messages.success(request, "Hotel created")
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
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel updated")
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
        messages.success(request, "Hotel deleted")
        return redirect('hotel_dashboard')
    return render(request, "hotels/hotel_confirm_delete.html", {"hotel": hotel})

# ✅ Public view: Anyone can see hotel list
def hotels_info(request):
    hotels = Hotel.objects.all()
    return render(request, "hotels/info.html", {"hotels": hotels})
