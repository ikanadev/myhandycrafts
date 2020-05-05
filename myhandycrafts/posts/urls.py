"""Maps urls"""
# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (
    PostViewSet,
    PostMediaViewSet
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'postmedias', PostMediaViewSet, basename='postmedias')

urlpatterns = [
    path('', include(router.urls)),
]
