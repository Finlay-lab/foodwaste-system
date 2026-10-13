from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationAdminForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "full_name", "role")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="password_hash",
        help_text="Hashed value stored in the password_hash column. It cannot be edited as plain text.",
    )

    class Meta:
        model = User
        fields = ("email", "full_name", "role", "password")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationAdminForm
    form = UserChangeAdminForm
    list_display = ("email", "full_name", "role", "created_at")
    list_filter = ("role",)
    search_fields = ("email", "full_name")
    ordering = ("full_name",)
    readonly_fields = ("id", "created_at", "password_hash_display")

    def get_form(self, request, obj=None, **kwargs):
        defaults = {"form": self.add_form if obj is None else self.form}
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (
                (
                    None,
                    {"fields": ("email", "full_name", "role", "password1", "password2")},
                ),
            )
        return (
            (None, {"fields": ("email", "password")}),
            ("Profile", {"fields": ("full_name", "role")}),
            ("Metadata", {"fields": ("id", "created_at", "password_hash_display")}),
        )

    @admin.display(description="password_hash")
    def password_hash_display(self, obj):
        return obj.password
