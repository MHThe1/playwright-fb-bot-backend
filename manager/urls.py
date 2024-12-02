from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActionViewSet
from .views import create_task_form

# Create a DRF router and register the ActionViewSet
router = DefaultRouter()
router.register(r'actions', ActionViewSet, basename='action')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    path('create_task_form', create_task_form, name='create_task_form'),
]
