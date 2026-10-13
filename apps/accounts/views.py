from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .decorators import system_administrator_required
from .forms import (
    AdminUserCreateForm,
    AdminUserUpdateForm,
    EmailAuthenticationForm,
    SignupForm,
)
from .models import User


class EmailLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.request.user.get_dashboard_url()


class EmailLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        User.login(request, user.email, form.cleaned_data["password1"])
        messages.success(request, "Account created. Welcome.")
        return redirect(user.get_dashboard_url())
    return render(request, "accounts/signup.html", {"form": form})


@system_administrator_required
def user_list(request):
    users = User.objects.all()
    return render(request, "accounts/user_list.html", {"users": users})


@system_administrator_required
@require_http_methods(["GET", "POST"])
def user_create(request):
    form = AdminUserCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "User created.")
        return redirect("accounts:user_list")
    return render(
        request,
        "accounts/user_form.html",
        {"form": form, "title": "Create user"},
    )


@system_administrator_required
@require_http_methods(["GET", "POST"])
def user_update(request, pk):
    account = get_object_or_404(User, pk=pk)
    form = AdminUserUpdateForm(request.POST or None, instance=account)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "User updated.")
        return redirect("accounts:user_list")
    return render(
        request,
        "accounts/user_form.html",
        {"form": form, "title": "Edit user", "account": account},
    )
