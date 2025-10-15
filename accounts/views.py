from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from guides.models import GuideProfile

User = get_user_model()


# ---------------------------
# SIGNUP VIEW
# ---------------------------
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Auto login
            return redirect('dashboard')  # Role-wise dashboard redirect
        else:
            # Optional: show form validation errors
            pass
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


# ---------------------------
# LOGIN VIEW
# ---------------------------
def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        user = None

        if '@' in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # role-wise dashboard
        else:
            messages.error(request, "Invalid username/email or password")

    return render(request, "accounts/login.html", {"messages": messages.get_messages(request)})
# ---------------------------
# LOGOUT VIEW
# ---------------------------
def logout_view(request):
    auth_logout(request)
    return redirect('login')


# ---------------------------
# DASHBOARD VIEW
# ---------------------------
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if hasattr(request.user, 'role'):
        if request.user.role == 'guide':
            return redirect('guide_dashboard')
        elif request.user.role == 'tourist':
            return redirect('tourist_home')
        elif request.user.role == 'hotel_manager':
            return redirect('hotel_dashboard')

    return redirect('guide_dashboard')