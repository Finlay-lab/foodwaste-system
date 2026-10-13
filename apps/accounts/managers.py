from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        extra_fields.setdefault("full_name", extra_fields.get("full_name") or "")
        if not extra_fields.get("full_name"):
            raise ValueError("Full name is required.")
        extra_fields.pop("is_staff", None)
        extra_fields.pop("is_superuser", None)
        extra_fields.pop("is_active", None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", self.model.Role.RESTAURANT_MANAGER)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields["role"] = self.model.Role.SYSTEM_ADMINISTRATOR
        extra_fields.setdefault("full_name", "System Administrator")
        return self._create_user(email, password, **extra_fields)
