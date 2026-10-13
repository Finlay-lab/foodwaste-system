from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    """Class-based view mixin: user must have one of ``allowed_roles``."""

    allowed_roles = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in self.allowed_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class RestaurantManagerRequiredMixin(RoleRequiredMixin):
    @property
    def allowed_roles(self):
        from .models import User

        return (User.Role.RESTAURANT_MANAGER,)


class InventoryStaffRequiredMixin(RoleRequiredMixin):
    @property
    def allowed_roles(self):
        from .models import User

        return (User.Role.INVENTORY_STAFF,)


class SystemAdministratorRequiredMixin(RoleRequiredMixin):
    @property
    def allowed_roles(self):
        from .models import User

        return (User.Role.SYSTEM_ADMINISTRATOR,)
