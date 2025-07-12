from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ClinicViewSet,
    InsurerViewSet,
    PharmacyViewSet,
    ConsultationViewSet,
    ContractViewSet,
    LoginView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'clinics', ClinicViewSet, basename='clinic')
router.register(r'insurers', InsurerViewSet, basename='insurer')
router.register(r'pharmacies', PharmacyViewSet, basename='pharmacy')
router.register(r'consultations', ConsultationViewSet, basename='consultation')
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
]
