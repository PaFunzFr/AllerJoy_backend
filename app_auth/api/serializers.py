from rest_framework import serializers
from app_auth.models import UserProfile
from app_allergens.api.serializers import CustomProfileAllergenSerializer
from app_allergens.models import CustomProfileAllergen
from django.contrib.auth.models import User
from app_auth.models import UserProfile, CustomProfile
from app_groups.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

MAX_FILE_SIZE = 2 * 1024 * 1024

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(
        write_only=True,
        help_text="Repeat the password for confirmation."
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'repeated_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True},
        }


    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    

    def validate(self, data):
        """Ensure passwords match."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        UserProfile.objects.create(user=user)
        
        return user

class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    # no response, if user exists
    def validate_email(self, value):
        return value


class ConfirmPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "username"in self.fields:
            self.fields.pop("username")


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        error_respone = "If registered, please confirm your email address before logging in. "\
                        "If you haven't signed up yet, please register first."

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(error_respone)

        if not user.is_active:
            raise serializers.ValidationError(error_respone)
        
        if not user.check_password(password):
            raise serializers.ValidationError(error_respone)
        
        # Authenticate using JWT
        data = super().validate({"username": user.username, "password": password})
        return data


class CustomProfileSerializer(serializers.ModelSerializer):
    allergens = CustomProfileAllergenSerializer(many=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = CustomProfile
        fields = ['id', 'nickname', 'groups', 'created_at', 'allergens', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']

    def validate(self, attrs):
        nickname = attrs.get('nickname')
        created_by = self.context['request'].user

        if CustomProfile.objects.filter(nickname=nickname, created_by=created_by).exists():
            raise serializers.ValidationError("This profile/nickname already exists")

        return attrs

    def create(self, validated_data):
        allergens_data = validated_data.pop('allergens', [])
        groups_data = validated_data.pop('groups', [])
        created_by = self.context['request'].user

        profile = CustomProfile.objects.create(created_by=created_by, **validated_data)

        if groups_data:
            profile.groups.set(groups_data)

        for allergen_data in allergens_data:
            CustomProfileAllergen.objects.create(
                custom_profile=profile, 
                **allergen_data
            )

        return profile
