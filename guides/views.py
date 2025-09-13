from django.shortcuts import render

# Create your views here.
def guides_info(request):
    return render(request,template_name='guides/guides_info.html')