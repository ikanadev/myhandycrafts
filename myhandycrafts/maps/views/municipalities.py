"""Municipalities views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny

# Serializer
from myhandycrafts.maps.serializers import (
    MunicipalityModelSerializer,
    MunicipalityListSerializer,
    MunicipalityDetailModelSerializer,
)

# models
from myhandycrafts.maps.models import Municipality


# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination


class MunicipalityViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Municipality view set."""

    serializer_class = MunicipalityModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
    ordering = ('name',)
    pagination_class = MyHandycraftsPageNumberPagination


    filter_fields = ['departament','province']
    # permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):
        """ queryset with filter departament, and province"""
        queryset = Municipality.objects.filter(active=True)

        if 'departament' in self.request.GET:
            queryset = queryset.filter(departament_id=self.request.GET.get('departament'))

        if 'province' in self.request.GET:
            queryset = queryset.filter(province_id=self.request.GET.get('province'))

        return queryset

    def get_serializer_class(self):
        if self.action in ['list','details']:
            return MunicipalityDetailModelSerializer
        return MunicipalityModelSerializer

    def get_serializer_context(self):
        return {
                'user':self.request.user,
                'fair':self.fair
                }

    def get_permissions(self):
        """Assing permision base on action."""
        permissions = []
        if self.action in ['create', 'update', 'destroy']:
            permissions.append(IsAdminUser)
        else:
            permissions.append(AllowAny)
        return [permission() for permission in permissions]


    def perform_destroy(self, instance):
        instance.active=False
        instance.deleted_at=timezone.now()
        instance.save()
        """add policies when object is deleted"""

    @action(detail=True, methods=['get'])
    def details(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MunicipalityListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = MunicipalityListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name','created_at', )

    def get_queryset(self):
        """ queryset with filter departament, and province"""
        queryset = Municipality.objects.filter(active=True)
        # for field in self.filter_fields:
        #     if field in self.request.GET:
        #         queryset.filter(self.request.GET.get(field))

        if 'departament' in self.request.GET:
            queryset = queryset.filter(departament_id=self.request.GET.get('departament'))

        if 'province' in self.request.GET:
            queryset = queryset.filter(province_id=self.request.GET.get('province'))

        return queryset

