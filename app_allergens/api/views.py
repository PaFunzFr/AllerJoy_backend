from rest_framework import generics
from .serializers import AllergensSerializer
from app_allergens.models import Allergen
from rest_framework.permissions import AllowAny, IsAuthenticated

class AllergensListView(generics.ListAPIView):
    queryset = Allergen.objects.all()
    serializer_class = AllergensSerializer
    permission_classes = []