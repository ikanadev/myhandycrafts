
# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (
    CategoryAdminViewSet,
    CategoryViewSet,
    CategoryListViewSet,
)

router = DefaultRouter()
router.register(r'a/categories', CategoryAdminViewSet, basename='admin/categories')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'categories_list', CategoryListViewSet, basename='categories_list')

urlpatterns = [
    path('', include(router.urls)),
]
