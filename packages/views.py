from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Package, Booking, Review
from .forms import BookingForm
from django.contrib import messages

def package_list(request):
    packages = Package.objects.all()
    return render(request, 'packages/package_list.html', {'packages': packages})



def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    reviews = package.reviews.all()

    # Preprocess text fields into lists
    itinerary_days = [line.strip() for line in package.itinerary.split('\n') if line.strip()]
    included_services_list = [line.strip() for line in package.included_services.split('\n') if line.strip()]
    exclusions_list = [line.strip() for line in package.exclusions.split('\n') if line.strip()]

    # ✅ Updated context with lists
    context = {
        'package': package,
        'reviews': reviews,
        'itinerary_days': itinerary_days,
        'included_services_list': included_services_list,
        'exclusions_list': exclusions_list,
    }

    # Render template with preprocessed data
    return render(request, 'packages/package_detail.html', context)

@login_required
def book_package(request, pk):
    package = get_object_or_404(Package, pk=pk)

    # Duplicate booking check
    if Booking.objects.filter(package=package, tourist=request.user).exists():
        messages.error(request, "You have already booked this package!")
        return redirect('package_detail', pk=pk)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Extra validation
            mobile = booking.mobile_number
            if not mobile:
                messages.error(request, "Mobile number is required!")
                return render(request, 'packages/book_package.html', {'form': form, 'package': package})

            people_count = booking.people_count
            if not people_count or people_count < 1:
                messages.error(request, "Please enter a valid number of people!")
                return render(request, 'packages/book_package.html', {'form': form, 'package': package})

            booking.package = package
            booking.tourist = request.user
            booking.save()
            messages.success(request, "Booking confirmed successfully!")
            return redirect('package_detail', pk=pk)
    else:
        form = BookingForm()

    return render(request, 'packages/book_package.html', {'form': form, 'package': package})

@login_required
def add_review(request, pk):
    if request.method == "POST":
        package = get_object_or_404(Package, pk=pk)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(package=package, tourist=request.user, rating=rating, comment=comment)
        messages.success(request, "Your review has been submitted successfully!")
        return redirect('package_detail', pk=pk)
