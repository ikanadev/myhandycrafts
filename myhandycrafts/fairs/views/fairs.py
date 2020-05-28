"""Fair views"""

# Djnago REST Framework
from rest_framework import viewsets,mixins,status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny

# models
from myhandycrafts.users.models import User
from myhandycrafts.maps.models import Departament,Province,Municipality
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


class FairAdminViewSet(viewsets.ModelViewSet):
    """Fair admin view set."""


    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = FairModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',
                     'description',
                     'municipality__name',
                     )
    ordering_fields = ( 'user',
                        'municipality',
                        'name',
                        'description',
                        'location',
                        'created_at',
                       )
    ordering = ('name',
                'user',
                'municipality',
                )
    pagination_class = MyHandycraftsPageNumberPagination

    def get_serializer_context(self):
        return {'user':self.request.user}


    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return FairDetailModelSerializer
        return FairModelSerializer

    def create(self, request, *args, **kwargs):
        """create province"""
        request.data['user']=self.request.user.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = FairDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        """update province"""
        instance  = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = FairDetailModelSerializer(instance).data
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

    def get_queryset(self):

        queryset =Fair.objects.filter(active=True)

        if 'user' in self.request.GET:
            try:
                user_id = int(self.request.GET.get('user'))
                user = User.objects.get(pk=user_id,active=True)
                queryset = queryset.filter(user=user)
            except (ValueError,User.DoesNotExist):
                queryset = []



        if 'departament' in self.request.GET:
            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id,active=True)
                queryset = queryset.filter(municipality__departament=departament)
            except (ValueError,Departament.DoesNotExist):
                queryset = []

        if 'province' in self.request.GET:
            try:
                province_id = int(self.request.GET.get('province'))
                province = Province.objects.get(pk=province_id,active=True)
                queryset = queryset.filter(municipality__province=province)
            except (ValueError,Province.DoesNotExist):
                queryset = []

        if 'municipality' in self.request.GET:
            try:
                municipality_id = int(self.request.GET.get('municipality'))
                municipality = Municipality.objects.get(pk=municipality_id, active=True)
                queryset = queryset.filter(municipality=municipality)
            except (ValueError, Municipality.DoesNotExist):
                queryset = []

        return queryset




class FairViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = Fair.objects.filter(active=True)
    serializer_class = FairDetailModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',
                     'description',
                     'municipality__name',
                     )
    ordering_fields = ('user',
                       'municipality',
                       'name',
                       'description',
                       'location',
                       'created_at',
                       )
    ordering = ('name',
                'user',
                'municipality',
                )
    pagination_class = MyHandycraftsPageNumberPagination

    def get_queryset(self):

        queryset =Fair.objects.filter(active=True)

        if 'user' in self.request.GET:
            try:
                user_id = int(self.request.GET.get('user'))
                user = User.objects.get(pk=user_id,active=True)
                queryset = queryset.filter(user=user)
            except (ValueError,User.DoesNotExist):
                queryset = []


        if 'departament' in self.request.GET:
            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id,active=True)
                queryset = queryset.filter(municipality__departament=departament)
            except (ValueError,Departament.DoesNotExist):
                queryset = []

        if 'province' in self.request.GET:
            try:
                province_id = int(self.request.GET.get('province'))
                province = Province.objects.get(pk=province_id,active=True)
                queryset = queryset.filter(municipality__province=province)
            except (ValueError,Province.DoesNotExist):
                queryset = []

        if 'municipality' in self.request.GET:
            try:
                municipality_id = int(self.request.GET.get('municipality'))
                municipality = Municipality.objects.get(pk=municipality_id, active=True)
                queryset = queryset.filter(municipality=municipality)
            except (ValueError, Municipality.DoesNotExist):
                queryset = []

        return queryset







class FairFeedViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):

    pagination_class = MyHandycraftsPageNumberPagination
    serializer_class = FairFeedModelSerializer


    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',
                     'description',
                     'municipality__name',
                     )
    ordering_fields = ('user',
                       'municipality',
                       'name',
                       'description',
                       'location',
                       'created_at',
                       )
    ordering = ('name',
                'user',
                'municipality',
                )
    pagination_class = MyHandycraftsPageNumberPagination

    def get_queryset(self):
        queryset = Fair.objects.filter(active=True)

        if 'user' in self.request.GET:
            try:
                user_id = int(self.request.GET.get('user'))
                user = User.objects.get(pk=user_id, active=True)
                queryset = queryset.filter(user=user)
            except (ValueError, User.DoesNotExist):
                queryset = []

        if 'departament' in self.request.GET:
            try:
                departament_id = int(self.request.GET.get('departament'))
                departament = Departament.objects.get(pk=departament_id, active=True)
                queryset = queryset.filter(municipality__departament=departament)
            except (ValueError, Departament.DoesNotExist):
                queryset = []

        if 'province' in self.request.GET:
            try:
                province_id = int(self.request.GET.get('province'))
                province = Province.objects.get(pk=province_id, active=True)
                queryset = queryset.filter(municipality__province=province)
            except (ValueError, Province.DoesNotExist):
                queryset = []

        if 'municipality' in self.request.GET:
            try:
                municipality_id = int(self.request.GET.get('municipality'))
                municipality = Municipality.objects.get(pk=municipality_id, active=True)
                queryset = queryset.filter(municipality=municipality)
            except (ValueError, Municipality.DoesNotExist):
                queryset = []

        return queryset



