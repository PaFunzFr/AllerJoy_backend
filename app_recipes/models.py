from django.db import models
from app_auth.models import UserProfile
from app_groups.models import Group
from app_allergens.models import Allergen

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField(blank=True)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_recipes')
    group = models.ManyToManyField(Group, related_name='recipes', blank=True)
    allergens = models.ManyToManyField(Allergen, blank=True, related_name='recipes')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return {self.title}
    
    def get_allergens(self):
        return self.allergens.all()


class RecipeRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name='ratings')
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='recipe_ratings')

    rating = models.PositiveSmallIntegerField(
        choices=[(1,1), (2,2), (3,3), (4,4), (5,5)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f"{self.user} rated {self.recipe} ({self.rating})"