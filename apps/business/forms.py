from django import forms

from .models import BusinessProfile


class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ("business_name", "business_type", "location", "contact_number")
        labels = {
            "business_name": "Business name",
            "business_type": "Business type",
            "location": "Location",
            "contact_number": "Contact number",
        }
        widgets = {
            "business_name": forms.TextInput(attrs={"class": "form-control"}),
            "business_type": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "contact_number": forms.TextInput(attrs={"class": "form-control"}),
        }
