from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActionViewSet

# Create a DRF router and register the ActionViewSet
router = DefaultRouter()
router.register(r'actions', ActionViewSet, basename='action')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]
