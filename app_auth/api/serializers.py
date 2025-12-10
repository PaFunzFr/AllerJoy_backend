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
    allergens = serializers.SerializerMethodField(read_only=True)
    add_allergens = CustomProfileAllergenSerializer(
        many=True, write_only=True, required=False
    )

    class Meta:
        model = CustomProfile
        fields = ['id', 'nickname', 'groups', 'created_at', 'created_by', 'allergens', 'add_allergens']
        read_only_fields = ['id', 'created_at', 'created_by', 'allergens']

    def validate(self, attrs):
        request = self.context["request"]


        nickname = attrs.get("nickname")
        if nickname is None:
            return attrs

        exists = CustomProfile.objects.filter(
            nickname=nickname,
            created_by=request.user
        ).exists()

        if exists:
            raise serializers.ValidationError({
                "nickname": "This nickname already exists for your profiles."
            })

        return attrs

    def get_allergens(self, obj):
        allergens = obj.profile_allergens.all()
        return CustomProfileAllergenSerializer(allergens, many=True).data

    def create(self, validated_data):
        request = self.context["request"]
        allergens_data = request.data.get("allergens", [])

        profile = CustomProfile.objects.create(
            created_by=request.user,
            **validated_data
        )

        for item in allergens_data:
            CustomProfileAllergen.objects.create(
                custom_profile=profile,
                allergen_id=item["allergen"],
                severity=item.get("severity", "medium")
            )

        return profile
