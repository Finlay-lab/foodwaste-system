from django import forms

from .models import FoodCategory


class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = ("category_name", "description")
        labels = {
            "category_name": "Category name",
            "description": "Description",
        }
        widgets = {
            "category_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
