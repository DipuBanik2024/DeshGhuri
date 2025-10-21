from .models import User

def user_role(request):
    """
    This context processor makes the logged-in user's info and role
    and notification count available in all templates automatically.
    """
    user = None
    role = None
    unread_notifications_count = 0

    if request.user.is_authenticated:
        user = request.user
        role = user.role  # from your custom User model field
        # Add notification count
        unread_notifications_count = user.notifications.filter(is_read=False).count()

    return {
        'logged_user': user,
        'logged_role': role,
        'unread_notifications_count': unread_notifications_count,
    }