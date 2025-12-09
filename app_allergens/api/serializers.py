from rest_framework import serializers
from app_allergens.models import Allergen

class AllergensSerializer(serializers.ModelSerializer):
    keywords_name = serializers.SerializerMethodField()

    class Meta:
        model = Allergen
        fields = ['id', 'name', 'category', 'keywords_name']

    def get_keywords_name(self, obj):
        return [k.keyword for k in obj.keywords.all()]