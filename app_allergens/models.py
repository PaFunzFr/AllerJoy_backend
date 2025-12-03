from django.db import models
from app_auth.models import UserProfile, CustomProfile

SEVERITY_CHOICES = [
    ("mild", "Mild"),
    ("medium", "Medium"),
    ("severe", "Severe"),
]

CATEGORY_CHOICES= [
    ("allergy", "Allergy"),
    ("intolerance", "Intolerance"),
    ("dislike", "Dislike")
]

class Allergen(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g. "milk", "gluten"
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="allergy")  # z.B. "allergy", "intolerance"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AllergenKeyword(models.Model):
    allergen = models.ForeignKey(Allergen, related_name="keywords", on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.keyword} ({self.allergen.name})"


class UserAllergen(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    allergen = models.ForeignKey(Allergen, on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="medium")

    class Meta:
        unique_together = ("user_profile", "allergen")


class CustomProfileAllergen(models.Model):
    custom_profile = models.ForeignKey(CustomProfile, on_delete=models.CASCADE)
    allergen = models.ForeignKey(Allergen, on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="medium")

    class Meta:
        unique_together = ("custom_profile", "allergen")