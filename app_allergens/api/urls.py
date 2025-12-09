from django.urls import path
from .views import AllergensListView


urlpatterns = [
    path('allergens/', AllergensListView.as_view(), name="allergens-list"),
]