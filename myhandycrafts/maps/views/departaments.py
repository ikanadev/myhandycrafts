"""Departaments views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny

# Serializer
from myhandycrafts.maps.serializers import (
    DepartamentModelSerializer,
    DepartamentListSerializer,
)

# models
from myhandycrafts.maps.models import Departament,Province,Municipality


# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination


class DepartamentViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Departament view set."""

    serializer_class = DepartamentModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
    ordering = ('name',)
    queryset = Departament.objects.filter(active=True)
    pagination_class = MyHandycraftsPageNumberPagination
    # permission_classes = [IsAuthenticated,IsAdminUser]

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
        # update Provinces
        Province.objects.filter(departament=instance
                                ).update(
                                    active=False,
                                    deleted_at=timezone.now()
                                    )
        # update Municipaly
        Municipality.objects.filter(departament=instance
                                ).update(
                                    active=False,
                                    deleted_at=timezone.now()
                                )



class DepartamentListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = DepartamentListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name','created_at', )
    queryset = Departament.objects.filter(active=True)




