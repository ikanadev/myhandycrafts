"""Fair views"""

# Djnago REST Framework
from rest_framework import viewsets,mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny

# models
from myhandycrafts.fairs.models import Fair

# Serializer
from myhandycrafts.fairs.serializers import (
    FairModelSerializer,
    FairDetailModelSerializer,
    FairFeedModelSerializer,
)

# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination



class FairViewSet(viewsets.ModelViewSet):

    queryset = Fair.objects.filter(active=True)
    # permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = FairModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name','created_at','date_init',)
    ordering = ('name',)
    pagination_class = MyHandycraftsPageNumberPagination

    def get_permissions(self):
        """Assing permision base on action."""
        permissions = []
        if self.action in ['create', 'update', 'destroy']:
            permissions.append(IsAdminUser)
        else:
            permissions.append(AllowAny)
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action in ['list','details']:
            return FairDetailModelSerializer
        return FairModelSerializer

    @action(detail=True, methods=['get'])
    def details(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""




class FairFeedViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):

    queryset = Fair.objects.filter(active=True)
    pagination_class = MyHandycraftsPageNumberPagination
    permission_classes = [AllowAny]
    serializer_class = FairFeedModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name','created_at','date_init',)
    ordering = ('name',)

