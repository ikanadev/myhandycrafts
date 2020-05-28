"""StorePost views."""

# Django
from django.utils import timezone

# Django REST Framework
from rest_framework import mixins,viewsets,status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response


# Utils
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination
# filters
from rest_framework.filters import SearchFilter,OrderingFilter

# Serializer
from myhandycrafts.posts.serializers import (
    StorePostModelSerializer,
    StorePostDetailModelSerializer,
)

# Model
from myhandycrafts.posts.models import StorePost
from myhandycrafts.users.models import User

class StorePostAdminViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """StorePost model view set."""
    serializer_class = StorePostModelSerializer
    pagination_class = MyHandycraftsPageNumberPagination
    permission_classes = [IsAuthenticated,IsAdminUser]

    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('user__username',
                     'user__first_name',
                     'user__last_name',
                     'store__name',
                     'post__title')
    ordering_fields = ('user',
                       'store',
                       'post',
                       'created_at',
                       )
    ordering = ('created_at','post','store','user',)

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return StorePostDetailModelSerializer
        return StorePostModelSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = StorePostDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

    def get_queryset(self):

        queryset = StorePost.objects.filter(active=True,
                                           user__active=True,
                                           post__active=True,
                                           store__active=True)
        if 'user' in self.request.GET:
            try:
                user_id = int(self.request.GET.get('user'))
                user = User.objects.get(pk=user_id,active=True)
                queryset = queryset.filter(user=user)
            except (ValueError, User.DoesNotExist):
                pass
        return queryset




class StorePostUserViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """StorePost model view set."""
    serializer_class = StorePostModelSerializer
    pagination_class = MyHandycraftsPageNumberPagination
    permission_classes = [IsAuthenticated]

    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('user__username',
                     'user__first_name',
                     'user__last_name',
                     'store__name',
                     'post__title')
    ordering_fields = ('user',
                       'store',
                       'post',
                       'created_at',
                       )
    ordering = ('created_at','post','store','user',)

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return StorePostDetailModelSerializer
        return StorePostModelSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = StorePostDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

    def get_queryset(self):
        user = self.request.user
        queryset = StorePost.objects.filter(user=user,
                                           active=True,
                                           user__active=True,
                                           post__active=True,
                                           store__active=True)

        return queryset


class StorePostViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """StorePost model view set."""
    serializer_class = StorePostModelSerializer
    pagination_class = MyHandycraftsPageNumberPagination


    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('user__username',
                     'user__first_name',
                     'user__last_name',
                     'store__name',
                     'post__title')
    ordering_fields = ('user',
                       'store',
                       'post',
                       'created_at',
                       )
    ordering = ('created_at','post','store','user',)

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return StorePostDetailModelSerializer
        return StorePostModelSerializer


    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

    def get_queryset(self):

        queryset = StorePost.objects.filter(active=True,
                                           user__active=True,
                                           post__active=True,
                                           store__active=True)

        return queryset