from django.shortcuts import render

# Create your views here.
def hotels_info(request):
    return render(request,template_name='hotels/hotels_info.html')