from rest_framework import serializers
from app_allergens.models import Allergen

class AllergensSerializer(serializers.ModelSerializer):
    keywords_name = serializers.SerializerMethodField()

    class Meta:
        model = Allergen
        fields = ['id', 'name', 'category', 'keywords_name']

    def validate_category(self, value):
        if value != "dislike":
            raise serializers.ValidationError("Invalid category")
        return value
    
    def validate(self, attrs):
        name = attrs.get('name')
        category = attrs.get('category')

        if Allergen.objects.filter(name__iexact=name, category=category).exists():
            raise serializers.ValidationError("This Dislike already exists")

        return attrs

    def get_keywords_name(self, obj):
        return [k.keyword for k in obj.keywords.all()]
    