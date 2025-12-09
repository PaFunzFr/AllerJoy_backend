from rest_framework import serializers
from app_allergens.models import Allergen, UserAllergen, CustomProfileAllergen

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


class UserAllergenSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField(read_only=True)
    allergen_name = serializers.SerializerMethodField(read_only=True)
    allergen = serializers.PrimaryKeyRelatedField(
        queryset=Allergen.objects.all(),
        write_only = True
    )

    class Meta:
        model = UserAllergen
        fields = ['id', 'username', 'allergen','allergen_name','severity','category']
        read_only_fields = ['id', 'username', 'allergen_name', 'category', 'allergen']
    
    def validate(self, attrs):
        allergen = attrs.get('allergen')
        severity = attrs.get('severity')

        if allergen.category != 'dislike' and not severity:
            raise serializers.ValidationError({
                'severity': "Please select severity for allergies and intolerances"
            })
        
        if not allergen:
            raise serializers.ValidationError("Allergen is required")

        return attrs
    
    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        allergen = validated_data['allergen']

        if UserAllergen.objects.filter(user_profile=user_profile, allergen=allergen).exists():
            raise serializers.ValidationError("This allergen is already added for this user.")

        validated_data['user_profile'] = user_profile
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.severity = validated_data.get('severity', instance.severity)
        instance.save()
        return instance
    
    def get_username(self, obj):
        return obj.user_profile.user.username
    
    def get_allergen_name(self, obj):
        return obj.allergen.name
    
    def get_category(self, obj):
        return obj.allergen.category
    

class UserAllergenDetailSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField(read_only=True)
    allergen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserAllergen
        fields = ['id', 'username','allergen','severity','category']
        read_only_fields = ['id', 'username', 'allergen', 'category', 'allergen']

    def update(self, instance, validated_data):
        instance.severity = validated_data.get('severity', instance.severity)
        instance.save()
        return instance
    
    def get_username(self, obj):
        return obj.user_profile.user.username
    
    def get_allergen(self, obj):
        return obj.allergen.name
    
    def get_category(self, obj):
        return obj.allergen.category


class CustomProfileAllergenSerializer(serializers.ModelSerializer):
    allergen_name = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    allergen = serializers.PrimaryKeyRelatedField(
        queryset=Allergen.objects.all()
    )
    custom_profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CustomProfileAllergen
        fields = ['id', 'custom_profile', 'allergen', 'allergen_name', 'severity', 'category']
        read_only_fields = ['id', 'custom_profile', 'allergen_name', 'category']

    def validate(self, attrs):
        allergen = attrs.get('allergen')
        severity = attrs.get('severity')

        if allergen.category != 'dislike' and not severity:
            raise serializers.ValidationError({
                'severity': "Please select severity for allergies and intolerances"
            })

        return attrs

    def create(self, validated_data):
        custom_profile = self.context.get('custom_profile')
        allergen = validated_data['allergen']

        if CustomProfileAllergen.objects.filter(custom_profile=custom_profile, allergen=allergen).exists():
            raise serializers.ValidationError("This allergen is already added for this profile.")

        validated_data['custom_profile'] = custom_profile
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.severity = validated_data.get('severity', instance.severity)
        instance.save()
        return instance

    def get_allergen_name(self, obj):
        return obj.allergen.name

    def get_category(self, obj):
        return obj.allergen.category