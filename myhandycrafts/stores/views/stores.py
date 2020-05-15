"""Store view."""
# Django REST Framework
from rest_framework import viewsets,mixins,status
from rest_framework.decorators import action
from rest_framework.response import Response

# permissions
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from myhandycrafts.stores.permissions import IsAdminorIsOwnerObject

# filters
from rest_framework.filters import SearchFilter,OrderingFilter

# Serializers
from myhandycrafts.stores.serializers import (
    StoreModelSerializer,
    StoreDetailModelSerializer,
)

# Models
from myhandycrafts.users.models import User
from myhandycrafts.stores.models import Store

# Django
from django.utils import timezone

#Pagination
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination


class StoreAdminViewSet(viewsets.ModelViewSet):
    """Store view set."""
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('name','description')
    ordering_fields = ('name',
                       'user',
                       'municipality',
                       'reputation',
                       'publications',
                       'visits',
                       'created_at',
                       )
    ordering =       ('name',
                       'user',
                       'municipality',
                       'reputation',
                       'publications',
                       'visits',
                       'created_at',
                      )
    pagination_class = MyHandycraftsPageNumberPagination
    permission_classes = [IsAdminUser]


    def get_serializer_context(self):
        return {'user':self.request.user}

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return StoreDetailModelSerializer
        return StoreModelSerializer

    def get_queryset(self):

        queryset =  Store.objects.filter(active=True)
        if 'user' in self.request.GET:
            try:
                user_id = int(self.request.GET.get('user'))
                user = User.objects.get(pk=user_id,active=True)
                queryset = queryset.filter(user=user)
            except (ValueError,User.DoesNotExist):
                queryset = []
        return queryset

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

    def create(self, request, *args, **kwargs):
        """create store"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = StoreDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        """update store"""
        instance  = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = StoreDetailModelSerializer(instance).data
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data, status=status.HTTP_200_OK)


class StoreUserViewSet(viewsets.ModelViewSet):
    """Store view set."""
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('name','description')
    ordering_fields = ('name',
                       'user',
                       'municipality',
                       'reputation',
                       'publications',
                       'visits',
                       'created_at',
                       )
    ordering =       ('name',
                       'user',
                       'municipality',
                       'reputation',
                       'publications',
                       'visits',
                       'created_at',
                      )
    pagination_class = MyHandycraftsPageNumberPagination
    permission_classes = [IsAuthenticated,IsAdminorIsOwnerObject]


    def get_serializer_context(self):
        return {'user':self.request.user}

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return StoreDetailModelSerializer
        return StoreModelSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Store.objects.filter(active=True,user=user)
        return  queryset

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

    def create(self, request, *args, **kwargs):
        """create store"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = StoreDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        """update store"""
        instance  = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = StoreDetailModelSerializer(instance).data
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data, status=status.HTTP_200_OK)





class StoreViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                   viewsets.GenericViewSet,):
    """Store public view set."""
    serializer_class = StoreDetailModelSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('name','description')
    ordering_fields = ('name',
                       'user',
                       'municipality',
                       'reputation',
                       'publications',
                       'visits',
                       'created_at',
                       )
    ordering = ('created_at',)
    filter_fields = ('user','municipality')
    queryset =  Store.objects.filter(active=True)
    pagination_class = MyHandycraftsPageNumberPagination

    def get_serializer_context(self):
        return {'user':self.request.user}


    def get_queryset(self):

        queryset = Store.objects.filter(active=True)
        if 'user' in self.request.GET:
            try:
                user_id = int(self.request.GET.get('user'))
                user = User.objects.get(pk=user_id, active=True)
                queryset = queryset.filter(user=user)
            except (ValueError, User.DoesNotExist):
                queryset = []
        return queryset





class StoreFeedViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet,
                       ):

    serializer_class = StoreDetailModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description','location')
    ordering_fields = ('name',
                       'user',
                       'municipality',
                       'reputation',
                       'publications',
                       'visits',
                       )
    ordering = ('name', 'updated_at')
    filter_fields = ('user', 'municipality')
    queryset = Store.objects.filter(active=True)
    pagination_class = MyHandycraftsPageNumberPagination
