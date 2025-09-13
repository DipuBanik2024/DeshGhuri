from django.shortcuts import render

# Create your views here.
def help_center(request):
    return render(request,template_name='helpline/help_center.html')