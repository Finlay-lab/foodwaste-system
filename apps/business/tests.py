from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.urls import reverse

from .models import BusinessProfile

User = get_user_model()
PASSWORD = "SecurePass123!"


class BusinessFactoryMixin:
    def make_user(self, email, role, full_name="Test User"):
        return User.objects.create_user(
            email=email,
            password=PASSWORD,
            full_name=full_name,
            role=role,
        )


class BusinessSchemaTests(TestCase):
    def test_business_profiles_table_matches_diagram(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'business_profiles'
                """
            )
            columns = {row[0] for row in cursor.fetchall()}
        self.assertIn("id", columns)
        self.assertIn("user_id", columns)
        self.assertIn("business_name", columns)
        self.assertIn("business_type", columns)
        self.assertIn("location", columns)
        self.assertIn("contact_number", columns)
        self.assertIn("registration_date", columns)


class BusinessProfileAccessTests(BusinessFactoryMixin, TestCase):
    def test_manager_can_register_profile(self):
        manager = self.make_user("mgr@example.com", User.Role.RESTAURANT_MANAGER)
        self.client.force_login(manager)
        response = self.client.post(
            reverse("business:manage"),
            {
                "business_name": "Green Plate",
                "business_type": "Restaurant",
                "location": "Nairobi",
                "contact_number": "0700000000",
            },
        )
        self.assertEqual(response.status_code, 302)
        profile = BusinessProfile.objects.get(owner=manager)
        self.assertEqual(profile.business_name, "Green Plate")
        self.assertEqual(profile.business_type, "Restaurant")
        self.assertTrue(profile.registration_date)

    def test_manager_can_update_profile(self):
        manager = self.make_user("mgr2@example.com", User.Role.RESTAURANT_MANAGER)
        BusinessProfile.register_business(
            manager,
            business_name="Old Name",
            business_type="Restaurant",
            location="Kisumu",
            contact_number="0711111111",
        )
        self.client.force_login(manager)
        response = self.client.post(
            reverse("business:manage"),
            {
                "business_name": "New Name",
                "business_type": "Hotel",
                "location": "Kisumu",
                "contact_number": "0711111111",
            },
        )
        self.assertEqual(response.status_code, 302)
        profile = BusinessProfile.objects.get(owner=manager)
        self.assertEqual(profile.business_name, "New Name")
        self.assertEqual(BusinessProfile.objects.filter(owner=manager).count(), 1)

    def test_staff_cannot_manage_profile(self):
        staff = self.make_user("staff@example.com", User.Role.INVENTORY_STAFF)
        self.client.force_login(staff)
        response = self.client.get(reverse("business:manage"))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_list_businesses(self):
        manager = self.make_user("owner@example.com", User.Role.RESTAURANT_MANAGER)
        BusinessProfile.register_business(
            manager,
            business_name="Campus Cafe",
            business_type="Cafeteria",
            location="Mombasa",
            contact_number="0722222222",
        )
        admin = self.make_user("adm@example.com", User.Role.SYSTEM_ADMINISTRATOR)
        self.client.force_login(admin)
        response = self.client.get(reverse("business:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Campus Cafe")

    def test_manager_cannot_open_admin_list(self):
        manager = self.make_user("mgr3@example.com", User.Role.RESTAURANT_MANAGER)
        self.client.force_login(manager)
        response = self.client.get(reverse("business:list"))
        self.assertEqual(response.status_code, 403)
