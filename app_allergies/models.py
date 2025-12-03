from django.db import models

class Allergen(models.Model):
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

    name = models.CharField(max_length=100, unique=True)  # e.g. "milk", "gluten"
    category = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="allergy")  # z.B. "allergy", "intolerance"
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="medium")

    def __str__(self):
        return self.name


class AllergenKeyword(models.Model):
    allergen = models.ForeignKey(Allergen, related_name="keywords", on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.keyword} ({self.allergen.name})"