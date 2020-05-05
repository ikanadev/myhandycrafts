"""Maps urls"""
# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (
    FairViewSet,
    FairMediaViewSet,
    ParticipantViewSet
)

router = DefaultRouter()
router.register(r'fairs', FairViewSet, basename='fairs')
router.register(r'fairmedias', FairMediaViewSet, basename='fairmedias')
router.register(r'fairparticipants', ParticipantViewSet, basename='participants')

urlpatterns = [
    path('', include(router.urls)),
]
