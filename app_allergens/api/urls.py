from django.urls import path
from .views import AllergensListCreateView, UserAllergensListCreateView, UserAllergensDetailView


urlpatterns = [
    path('allergens/', AllergensListCreateView.as_view(), name="allergens-list"),
    path('userallergens/', UserAllergensListCreateView.as_view(), name='userallergens-list-create'),
    path('userallergens/<int:pk>/', UserAllergensDetailView.as_view(), name='userallergens-detail'),
]