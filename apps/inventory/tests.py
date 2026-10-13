from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.urls import reverse

from .models import FoodCategory

User = get_user_model()
PASSWORD = "SecurePass123!"


class InventoryFactoryMixin:
    def make_user(self, email, role, full_name="Test User"):
        return User.objects.create_user(
            email=email,
            password=PASSWORD,
            full_name=full_name,
            role=role,
        )


class FoodCategorySchemaTests(TestCase):
    def test_food_categories_table_matches_diagram(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'food_categories'
                """
            )
            columns = {row[0] for row in cursor.fetchall()}
        self.assertIn("id", columns)
        self.assertIn("category_name", columns)
        self.assertIn("description", columns)


class FoodCategoryAccessTests(InventoryFactoryMixin, TestCase):
    def test_admin_can_create_category(self):
        admin = self.make_user("adm@example.com", User.Role.SYSTEM_ADMINISTRATOR)
        self.client.force_login(admin)
        response = self.client.post(
            reverse("inventory:category_create"),
            {
                "category_name": "Produce",
                "description": "Fresh fruit and vegetables",
            },
        )
        self.assertEqual(response.status_code, 302)
        category = FoodCategory.objects.get(category_name="Produce")
        self.assertEqual(category.description, "Fresh fruit and vegetables")

    def test_admin_can_update_category(self):
        admin = self.make_user("adm2@example.com", User.Role.SYSTEM_ADMINISTRATOR)
        category = FoodCategory.objects.create(
            category_name="Dairy",
            description="Milk products",
        )
        self.client.force_login(admin)
        response = self.client.post(
            reverse("inventory:category_update", args=[category.pk]),
            {
                "category_name": "Dairy",
                "description": "Milk, cheese, yoghurt",
            },
        )
        self.assertEqual(response.status_code, 302)
        category.refresh_from_db()
        self.assertEqual(category.description, "Milk, cheese, yoghurt")

    def test_admin_can_delete_category(self):
        admin = self.make_user("adm3@example.com", User.Role.SYSTEM_ADMINISTRATOR)
        category = FoodCategory.objects.create(category_name="Bakery", description="")
        self.client.force_login(admin)
        response = self.client.post(
            reverse("inventory:category_delete", args=[category.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FoodCategory.objects.filter(pk=category.pk).exists())

    def test_admin_can_list_categories(self):
        admin = self.make_user("adm4@example.com", User.Role.SYSTEM_ADMINISTRATOR)
        FoodCategory.objects.create(category_name="Meat", description="")
        self.client.force_login(admin)
        response = self.client.get(reverse("inventory:category_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Meat")

    def test_manager_cannot_manage_categories(self):
        manager = self.make_user("mgr@example.com", User.Role.RESTAURANT_MANAGER)
        self.client.force_login(manager)
        response = self.client.get(reverse("inventory:category_list"))
        self.assertEqual(response.status_code, 403)

    def test_staff_cannot_manage_categories(self):
        staff = self.make_user("staff@example.com", User.Role.INVENTORY_STAFF)
        self.client.force_login(staff)
        response = self.client.get(reverse("inventory:category_list"))
        self.assertEqual(response.status_code, 403)
