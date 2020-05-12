"""Store view."""
# Django REST Framework
from rest_framework import viewsets,mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
from myhandycrafts.stores.permissions import IsAdminorIsOwnerObject

# filters
from rest_framework.filters import SearchFilter,OrderingFilter

# Serializers
from myhandycrafts.stores.serializers import (
    StoreModelSerializer,
    StoreDetailSerializer,
)

# Models
from myhandycrafts.stores.models import Store

# Django
from django.utils import timezone

#Pagination
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination

class StoreViewSet(viewsets.ModelViewSet):
    """Store view set."""
    serializer_class = StoreModelSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('name','description')
    ordering_fields = ('name',
                       'user',
                       'municipality',
                       'reputation',
                       'publications',
                       'visits',
                       )
    ordering = ('name','updated_at')
    filter_fields = ('user','municipality')
    queryset =  Store.objects.filter(active=True)
    pagination_class = MyHandycraftsPageNumberPagination

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['create','update','destroy']:
            permissions = [IsAuthenticated,IsAdminorIsOwnerObject]
        else:
            permissions =[AllowAny]
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'user':self.request.user}

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""


    @action(detail=True, methods=['get'])
    def details(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StoreDetailSerializer(instance)
        return Response(serializer.data)



class StoreFeedViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet,
                       ):

    serializer_class = StoreDetailSerializer
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
