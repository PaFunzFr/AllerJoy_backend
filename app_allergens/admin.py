from django.contrib import admin
from app_allergens.models import Allergen, AllergenKeyword, UserAllergen

class AllergenKeywordInline(admin.TabularInline):
    model = AllergenKeyword
    extra = 1
    verbose_name = "Keyword"
    verbose_name_plural = "Keywords"

@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'keywords_list')
    list_filter = ('category',)
    search_fields = ('name', 'keywords__keyword')
    inlines = [AllergenKeywordInline]

    def keywords_list(self, obj):
        return ", ".join(k.keyword for k in obj.keywords.all())
    
    keywords_list.short_description = "Keywords"

@admin.register(UserAllergen)
class UserAllergenAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'allergen', 'severity')
    search_fields = ('user_profile', 'allergen')