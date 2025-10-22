from django.shortcuts import render
from destinations.models import Destination
from packages.models import Package
from guides.models import GuideProfile
from hotels.models import Hotel
def home(request):
    destinations = Destination.objects.all()[:6]
    packages = Package.objects.all()[:6]
    guides = GuideProfile.objects.all()[:6]
    hotels = Hotel.objects.all()[:6]

    for package in packages:
        package.avg_rating = package.average_rating()
        package.review_count_num = package.review_count()

    context = {
        'destinations': destinations,
        'packages': packages,
        'guides': guides,
        'hotels': hotels,
    }
    return render(request, 'main/home.html', context)
