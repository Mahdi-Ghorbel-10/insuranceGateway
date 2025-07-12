from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VaultViewSet

router = DefaultRouter()
router.register(r'vault', VaultViewSet, basename='vault')

urlpatterns = [
    path('', include(router.urls)),
]
