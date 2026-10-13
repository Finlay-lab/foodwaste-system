from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """Allow access only to authenticated users whose role is in ``roles``."""

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def restaurant_manager_required(view_func):
    from .models import User

    return role_required(User.Role.RESTAURANT_MANAGER)(view_func)


def inventory_staff_required(view_func):
    from .models import User

    return role_required(User.Role.INVENTORY_STAFF)(view_func)


def system_administrator_required(view_func):
    from .models import User

    return role_required(User.Role.SYSTEM_ADMINISTRATOR)(view_func)
