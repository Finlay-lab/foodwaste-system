import uuid

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.functions import Now
from django.urls import reverse

from .managers import UserManager


class User(AbstractBaseUser):
    """Custom user matching Figure 2 (class User) and Figure 7 (table users)."""

    class Role(models.TextChoices):
        RESTAURANT_MANAGER = "restaurant_manager", "Restaurant Manager"
        INVENTORY_STAFF = "inventory_staff", "Inventory Staff"
        SYSTEM_ADMINISTRATOR = "system_administrator", "System Administrator"

    REGISTERABLE_ROLES = (
        Role.RESTAURANT_MANAGER,
        Role.INVENTORY_STAFF,
    )

    last_login = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=155)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, db_column="password_hash")
    role = models.CharField(max_length=32, choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True, db_default=Now())

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
    EMAIL_FIELD = "email"

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["full_name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    role__in=[
                        "restaurant_manager",
                        "inventory_staff",
                        "system_administrator",
                    ]
                ),
                name="users_role_check",
            ),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    @property
    def is_staff(self):
        return self.role == self.Role.SYSTEM_ADMINISTRATOR

    @property
    def is_superuser(self):
        return self.role == self.Role.SYSTEM_ADMINISTRATOR

    @property
    def is_restaurant_manager(self):
        return self.role == self.Role.RESTAURANT_MANAGER

    @property
    def is_inventory_staff(self):
        return self.role == self.Role.INVENTORY_STAFF

    @property
    def is_system_administrator(self):
        return self.role == self.Role.SYSTEM_ADMINISTRATOR

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_all_permissions(self, obj=None):
        return set()

    def get_group_permissions(self, obj=None):
        return set()

    def get_user_permissions(self, obj=None):
        return set()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.email

    def get_dashboard_url(self):
        if self.is_system_administrator:
            return reverse("dashboard:system_administrator")
        if self.is_inventory_staff:
            return reverse("dashboard:inventory_staff")
        return reverse("dashboard:restaurant_manager")

    @classmethod
    def login(cls, request, email, password):
        """Class operation from Figure 2: login(email, password): Boolean."""
        user = authenticate(request, username=email, password=password)
        if user is None:
            return False
        django_login(request, user)
        return True

    def logout(self, request):
        """Instance operation from Figure 2: logout()."""
        django_logout(request)
