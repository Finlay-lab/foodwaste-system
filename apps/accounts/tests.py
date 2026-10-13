from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

PASSWORD = "SecurePass123!"


class UserFactoryMixin:
    def make_user(self, email, role, full_name="Test User", password=PASSWORD):
        return User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            role=role,
        )


class UserModelTests(UserFactoryMixin, TestCase):
    def test_password_is_hashed_not_plaintext(self):
        user = self.make_user("hash@example.com", User.Role.RESTAURANT_MANAGER)
        user.refresh_from_db()
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))
        self.assertTrue(
            user.password.startswith("pbkdf2_sha256$")
            or user.password.startswith("argon2")
            or user.password.startswith("bcrypt")
            or user.password.startswith("scrypt$")
        )

    def test_users_table_matches_schema(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'users'
                """
            )
            columns = {row[0] for row in cursor.fetchall()}
        self.assertIn("id", columns)
        self.assertIn("full_name", columns)
        self.assertIn("email", columns)
        self.assertIn("password_hash", columns)
        self.assertIn("role", columns)
        self.assertIn("created_at", columns)
        self.assertNotIn("password", columns)

    def test_create_superuser_is_system_administrator(self):
        admin = User.objects.create_superuser(
            email="admin-model@example.com",
            password=PASSWORD,
            full_name="Admin User",
        )
        self.assertEqual(admin.role, User.Role.SYSTEM_ADMINISTRATOR)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class SignupTests(TestCase):
    def test_signup_manager_and_login(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "full_name": "Pat Manager",
                "email": "manager@example.com",
                "role": User.Role.RESTAURANT_MANAGER,
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="manager@example.com")
        self.assertEqual(user.role, User.Role.RESTAURANT_MANAGER)
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))
        self.assertEqual(response.url, reverse("dashboard:restaurant_manager"))

    def test_cannot_signup_as_system_administrator(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "full_name": "Evil Admin",
                "email": "evil@example.com",
                "role": User.Role.SYSTEM_ADMINISTRATOR,
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email="evil@example.com").exists())


class LoginLogoutTests(UserFactoryMixin, TestCase):
    def setUp(self):
        self.user = self.make_user(
            "staff@example.com",
            User.Role.INVENTORY_STAFF,
            full_name="Sam Staff",
        )

    def test_login_success_redirects_to_role_dashboard(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "staff@example.com", "password": PASSWORD},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard:inventory_staff"))

    def test_login_rejects_wrong_password(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "staff@example.com", "password": "WrongPass123!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username="staff@example.com", password=PASSWORD)
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("dashboard:inventory_staff"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)


class AccessControlTests(UserFactoryMixin, TestCase):
    def setUp(self):
        self.manager = self.make_user(
            "mgr@example.com", User.Role.RESTAURANT_MANAGER, "Rita Manager"
        )
        self.staff = self.make_user(
            "inv@example.com", User.Role.INVENTORY_STAFF, "Ian Staff"
        )
        self.admin = self.make_user(
            "sys@example.com", User.Role.SYSTEM_ADMINISTRATOR, "Ada Admin"
        )

    def test_unauthenticated_dashboard_redirects_to_login(self):
        response = self.client.get(reverse("dashboard:restaurant_manager"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_manager_cannot_access_user_accounts(self):
        self.client.login(username="mgr@example.com", password=PASSWORD)
        response = self.client.get(reverse("accounts:user_list"))
        self.assertEqual(response.status_code, 403)

    def test_staff_cannot_access_admin_dashboard(self):
        self.client.login(username="inv@example.com", password=PASSWORD)
        response = self.client.get(reverse("dashboard:system_administrator"))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_manage_users(self):
        self.client.login(username="sys@example.com", password=PASSWORD)
        response = self.client.get(reverse("accounts:user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ada Admin")

    def test_admin_can_create_administrator(self):
        self.client.login(username="sys@example.com", password=PASSWORD)
        response = self.client.post(
            reverse("accounts:user_create"),
            {
                "full_name": "New Admin",
                "email": "newadmin@example.com",
                "role": User.Role.SYSTEM_ADMINISTRATOR,
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)
        created = User.objects.get(email="newadmin@example.com")
        self.assertEqual(created.role, User.Role.SYSTEM_ADMINISTRATOR)
        self.assertNotEqual(created.password, PASSWORD)

    def test_role_mismatch_on_manager_dashboard(self):
        self.client.login(username="inv@example.com", password=PASSWORD)
        response = self.client.get(reverse("dashboard:restaurant_manager"))
        self.assertEqual(response.status_code, 403)


class ApiPermissionTests(TestCase):
    def test_health_is_public(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_api_requires_authentication(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 403)
