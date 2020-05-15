"""Provinces views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
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
from myhandycrafts.maps.models import Departament,Province,Municipality


# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination


class ProvinceAdminViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Province view set."""
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('name',)
    ordering_fields = ('name','departament','created_at')
    ordering = ('name',)
    pagination_class = MyHandycraftsPageNumberPagination
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):
        queryset = Province.objects.filter(active=True)
        if 'departament' in self.request.GET:
            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id,active=True)
                queryset = queryset.filter(departament=departament)
            except (ValueError,Departament.DoesNotExist):
                queryset=[]
        return queryset

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return ProvinceDetailModelSerializer
        return ProvinceModelSerializer

    def create(self, request, *args, **kwargs):
        """create province"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = ProvinceDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        """update province"""
        instance  = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = ProvinceDetailModelSerializer(instance).data
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data, status=status.HTTP_200_OK)

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




class ProvinceViewSet(   mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Province view set."""
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('name',)
    ordering_fields = ('name','departament','created_at')
    ordering = ('name',)
    serializer_class = ProvinceDetailModelSerializer

    def get_queryset(self):
        queryset = Province.objects.filter(active=True)
        if 'departament' in self.request.GET:
            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id, active=True)
                queryset = queryset.filter(departament=departament)
            except (ValueError, Departament.DoesNotExist):
                queryset =[]
        return queryset



class ProvinceListViewSet(
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Province view set."""
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('name',)
    ordering_fields = ('name','departament','created_at')
    ordering = ('name',)
    serializer_class = ProvinceListSerializer

    def get_queryset(self):
        queryset = Province.objects.filter(active=True)
        if 'departament' in self.request.GET:
            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id, active=True)
                queryset = queryset.filter(departament=departament)
            except (ValueError, Departament.DoesNotExist):
                queryset =[]
        return queryset


