"""Store url."""

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (
    StoreAdminViewSet,
    StoreUserViewSet,
    StoreViewSet,
    StoreMediaViewSet,
    StoreFeedViewSet,
)

router = DefaultRouter()
router.register(r'a/stores', StoreAdminViewSet, basename='stores')
router.register(r'u/stores', StoreUserViewSet, basename='stores')
router.register(r'stores', StoreViewSet, basename='stores')
router.register(r'stores_feed', StoreFeedViewSet, basename='stores')
router.register(r'storemedias', StoreMediaViewSet, basename='storemedias')

urlpatterns = [
    path('', include(router.urls)),
]

