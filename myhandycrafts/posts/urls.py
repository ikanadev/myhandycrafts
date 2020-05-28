"""Maps urls"""
# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (
    PostAdminViewSet,
    PostUserViewSet,
    PostViewSet,
    PostMediaViewSet,
    FairPostAdminViewSet,
    FairPostViewSet,
    FairPostUserViewSet,
    StorePostAdminViewSet,
    StorePostViewSet,
    StorePostUserViewSet,
)

router = DefaultRouter()
router.register(r'a/posts', PostAdminViewSet, basename='posts')
router.register(r'u/posts', PostUserViewSet, basename='posts')
router.register(r'posts', PostViewSet, basename='posts')

router.register(r'postmedias', PostMediaViewSet, basename='postmedias')

router.register(r'a/fairposts', FairPostAdminViewSet, basename='fairposts')
router.register(r'u/fairposts', FairPostUserViewSet, basename='fairposts')
router.register(r'fairposts', FairPostViewSet, basename='fairposts')

router.register(r'a/storeposts',StorePostAdminViewSet, basename='storeposts')
router.register(r'u/storeposts',StorePostUserViewSet, basename='storeposts')
router.register(r'storeposts',StorePostViewSet, basename='storeposts')

urlpatterns = [
    path('', include(router.urls)),
]
