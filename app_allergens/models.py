from django.db import models

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
    name = models.CharField(max_length=100)  # e.g. "milk", "gluten"
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default="allergy")  # z.B. "allergy", "intolerance"
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("name", "category")

    def __str__(self):
        return self.name


class AllergenKeyword(models.Model):
    allergen = models.ForeignKey("app_allergens.Allergen", related_name="keywords", on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.keyword} ({self.allergen.name})"


class UserAllergen(models.Model):
    user_profile = models.ForeignKey("app_auth.UserProfile", on_delete=models.CASCADE)
    allergen = models.ForeignKey("app_allergens.Allergen", on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="medium")

    class Meta:
        unique_together = ("user_profile", "allergen")


class CustomProfileAllergen(models.Model):
    custom_profile = models.ForeignKey("app_auth.CustomProfile", on_delete=models.CASCADE)
    allergen = models.ForeignKey("app_allergens.Allergen", on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="medium")

    class Meta:
        unique_together = ("custom_profile", "allergen")