"""Municipalities views."""

# Django REST Framework
from rest_framework import mixins, viewsets,status
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
from myhandycrafts.maps.models import (
    Departament,
    Province,
    Municipality,
)



# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination



class MunicipalityAdminViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Municipality view set."""


    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',
                       'departament',
                       'province',
                       'created_at',
                       )
    ordering =        ('name',
                       'departament',
                       'province',
                       'created_at',
                       )
    pagination_class = MyHandycraftsPageNumberPagination
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return MunicipalityDetailModelSerializer
        return MunicipalityModelSerializer

    def get_serializer_context(self):
        return {
                'user':self.request.user
                }

    def get_queryset(self):
        """ queryset with filter departament, and province"""
        queryset = Municipality.objects.filter(active=True)

        if 'departament' in self.request.GET:

            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id, active=True)
                queryset = queryset.filter(departament=departament)
            except (ValueError, Departament.DoesNotExist):
                queryset = []

        elif 'province' in self.request.GET:
            try:
                province_id = int(self.request.GET.get('province'))
                province = Province.objects.get(pk=province_id, active=True)
                queryset = queryset.filter(province=province)
            except (ValueError, Province.DoesNotExist):
                queryset = []

        return queryset

    def create(self, request, *args, **kwargs):
        """Create municipality"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = MunicipalityDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        """update province"""
        instance  = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = MunicipalityDetailModelSerializer(instance).data
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""




class MunicipalityViewSet(   mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    """Municipality view set."""

    serializer_class = MunicipalityDetailModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',
                       'departament',
                       'province',
                       'created_at',
                       )
    ordering = ('name',
                'departament',
                'province',
                'created_at',
                )

    def get_queryset(self):
        """ queryset with filter departament, and province"""
        queryset = Municipality.objects.filter(active=True)

        if 'departament' in self.request.GET:

            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id, active=True)
                queryset = queryset.filter(departament=departament)
            except (ValueError, Departament.DoesNotExist):
                queryset = []

        elif 'province' in self.request.GET:
            try:
                province_id = int(self.request.GET.get('province'))
                province = Province.objects.get(pk=province_id, active=True)
                queryset = queryset.filter(province=province)
            except (ValueError, Province.DoesNotExist):
                queryset = []

        return queryset


class MunicipalityListViewSet(  mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = MunicipalityListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',
                       'departament',
                       'province',
                       'created_at',
                       )
    ordering = ('name',
                'departament',
                'province',
                'created_at',
                )

    def get_queryset(self):
        """ queryset with filter departament, and province"""
        queryset = Municipality.objects.filter(active=True)

        if 'departament' in self.request.GET:

            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id, active=True)
                queryset = queryset.filter(departament=departament)
            except (ValueError, Departament.DoesNotExist):
                queryset = []

        elif 'province' in self.request.GET:
            try:
                province_id = int(self.request.GET.get('province'))
                province = Province.objects.get(pk=province_id, active=True)
                queryset = queryset.filter(province=province)
            except (ValueError, Province.DoesNotExist):
                queryset = []

        return queryset

