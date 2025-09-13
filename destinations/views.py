from django.shortcuts import render

# Create your views here.
def destinations_info(request):
    return render(request,template_name='destinations/destinations_info.html')