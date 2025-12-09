from django.urls import path
from .views import AllergensListCreateView, UserAllergensListCreateView, UserAllergensDetailView


urlpatterns = [
    path('allergens/', AllergensListCreateView.as_view(), name="allergens-list"),
    path('user-allergens/', UserAllergensListCreateView.as_view(), name='userallergens-list-create'),
    path('user-allergens/<int:pk>/', UserAllergensDetailView.as_view(), name='userallergens-detail'),
    path('custom-allergens/', UserAllergensListCreateView.as_view(), name='userallergens-list-create'),
    path('custom-allergens/<int:pk>/', UserAllergensDetailView.as_view(), name='userallergens-detail'),
]