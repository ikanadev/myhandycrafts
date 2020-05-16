"""Maps urls"""
# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (
    FairAdminViewSet,
    FairViewSet,
    FairFeedViewSet,
    FairMediaViewSet,
    ParticipantAdminViewSet,
    ParticipantViewSet,
)

router = DefaultRouter()

router.register(r'a/fairs', FairAdminViewSet, basename='fairs')
router.register(r'fairs', FairViewSet, basename='fairs')
router.register(r'a/fairs/(?P<fair_id>[0-9]+)/participant',
    ParticipantAdminViewSet,
    basename='participantadmin'
)
router.register(r'fairs/(?P<fair_id>[0-9]+)/participants',
    ParticipantViewSet,
    basename='participants'
)
router.register(r'fairs_feed', FairFeedViewSet, basename='fairs')
router.register(r'fairmedias', FairMediaViewSet, basename='fairmedias')
# router.register(r'fairparticipants', ParticipantViewSet, basename='participants')

urlpatterns = [
    path('', include(router.urls)),
]
