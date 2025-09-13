from django.shortcuts import render

# Create your views here.
def packages_info(request):
    return render(request,template_name='packages/packages_info.html')