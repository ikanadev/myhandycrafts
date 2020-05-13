"""Provinces views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny


# Serializer
from myhandycrafts.maps.serializers import (
    ProvinceModelSerializer,
    ProvinceListSerializer,
    ProvinceDetailModelSerializer
)

# models
from myhandycrafts.maps.models import Province,Municipality


# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination

class ProvinceViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Province view set."""

    # serializer_class = ProvinceModelSerializer
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('name',)
    ordering_fields = ('name',)
    ordering = ('name',)
    pagination_class = MyHandycraftsPageNumberPagination




    # filter_fields = ['departament']
    # permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):
        queryset = Province.objects.filter(active=True)
        if 'departament' in self.request.GET:
            return queryset.filter(departament_id=self.request.GET.get('departament'))
        return queryset

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
            return ProvinceDetailModelSerializer
        return ProvinceModelSerializer

    def perform_destroy(self, instance):
        instance.active=False
        instance.deleted_at=timezone.now()
        instance.save()
        """add policies when object is deleted"""
        # update Municipaly
        Municipality.objects.filter(province=instance
                                        ).update(
                                            active=False,
                                            deleted_at=timezone.now()
                                        )

    @action(detail=True, methods=['get'])
    def details(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProvinceListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = ProvinceListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name','created_at', )
    queryset = Province.objects.filter(active=True)


