from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from .forms import ContactForm

# Create your views here.
def help_center(request):
    return render (request,template_name='helpline/help_center.html')

def privacy_policy(request):
    return render (request,template_name='helpline/privacy_policy.html')

def services(request):
    return render (request,template_name='helpline/services.html')

def terms(request):
    return render (request,template_name='helpline/terms.html')




def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'helpline/contact.html', {'form': form})