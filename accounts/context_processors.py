from .models import User

def user_role(request):
    """
    This context processor makes the logged-in user's info and role
    available in all templates automatically.
    """
    user = None
    role = None

    if request.user.is_authenticated:
        user = request.user
        role = user.role  # from your custom User model field

    return {
        'logged_user': user,
        'logged_role': role,
    }
