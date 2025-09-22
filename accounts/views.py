from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

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
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


# ---------------------------
# LOGIN VIEW
# ---------------------------
def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')  # username or email
        password = request.POST.get('password')
        user = None

        if '@' in identifier:  # login with email
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:  # fallback: login with username
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            auth_login(request, user)  # use alias to avoid conflict
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username/email or password")

    return render(request, "accounts/login.html")


# ---------------------------
# LOGOUT VIEW
# ---------------------------
def logout_view(request):
    auth_logout(request)  # use alias
    messages.success(request, "You have been logged out.")
    return redirect('login')


# ---------------------------
# DASHBOARD VIEW
# ---------------------------
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_guide():
        return render(request, "accounts/guide_dashboard.html")
    elif request.user.is_tourist():
        return render(request, "accounts/tourist_dashboard.html")
    elif request.user.is_hotel_manager():
        return render(request, "accounts/hotel_dashboard.html")

    # fallback dashboard
    return render(request, "accounts/dashboard.html")
