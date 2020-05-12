"""Maps urls"""
# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (
    DepartamentViewSet,
    DepartamentListViewSet,
    ProvinceViewSet,
    ProvinceListViewSet,
    MunicipalityViewSet,
    MunicipalityListViewSet,
)

router = DefaultRouter()
router.register(r'maps/departaments', DepartamentViewSet, basename='departaments')
router.register(r'maps/departaments_list', DepartamentListViewSet, basename='departaments')
router.register(r'maps/provinces', ProvinceViewSet, basename='provinces')
router.register(r'maps/provinces_list', ProvinceListViewSet, basename='provinces')
router.register(r'maps/municipalities', MunicipalityViewSet, basename='municipalities')
router.register(r'maps/municipalities_list', MunicipalityListViewSet, basename='municipalities')

urlpatterns = [
    path('', include(router.urls)),
]
