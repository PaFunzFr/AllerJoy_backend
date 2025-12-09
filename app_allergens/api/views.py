from rest_framework import generics, viewsets
from .serializers import AllergensSerializer, UserAllergenSerializer, UserAllergenDetailSerializer
from app_allergens.models import Allergen, UserAllergen
from rest_framework.permissions import AllowAny, IsAuthenticated

class AllergensListCreateView(generics.ListCreateAPIView):
    queryset = Allergen.objects.all()
    serializer_class = AllergensSerializer
    permission_classes = []


class UserAllergensListCreateView(generics.ListCreateAPIView):
    serializer_class = UserAllergenSerializer
    permission_classes = []

    def get_queryset(self):
        return UserAllergen.objects.filter(user_profile=self.request.user.profile)


class UserAllergensDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAllergenDetailSerializer
    permission_classes = []
    lookup_field = 'pk'

    def get_queryset(self):
        return UserAllergen.objects.filter(user_profile=self.request.user.profile)