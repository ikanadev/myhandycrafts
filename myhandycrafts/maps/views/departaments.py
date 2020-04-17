"""Departaments views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Serializer
from myhandycrafts.maps.serializers import DepartamentModelSerializer

# models
from myhandycrafts.maps.models import Departament,Province,Municipality


# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend


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
    queryset = Departament.objects.filter(is_deleted=False)
    # permission_classes = [IsAuthenticated,IsAdminUser]

    def get_permissions(self):
        """Assing permision based onm action"""
        if self.action in ['create','update','partial_update']:
            permissions =[IsAuthenticated,IsAdminUser]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def perform_destroy(self, instance):
        instance.is_deleted=True
        instance.deleted_at=timezone.now()
        instance.save()
        """add policies when object is deleted"""
        # update Provinces
        Province.objects.filter(departament=instance
                                ).update(
                                    is_deleted=True,
                                    deleted_at=timezone.now()
                                    )
        # update Municipaly
        Municipality.objects.filter(departament=instance
                                ).update(
                                    is_deleted=True,
                                    deleted_at=timezone.now()
                                )





