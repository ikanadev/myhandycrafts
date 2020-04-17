"""Departaments views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Serializer
from myhandycrafts.maps.serializers import ProvinceModelSerializer

# models
from myhandycrafts.maps.models import Province,Municipality


# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ProvinceViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Province view set."""

    serializer_class = ProvinceModelSerializer
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('name',)
    ordering_fields = ('name',)
    ordering = ('name',)
    # queryset = Province.objects.filter(is_deleted=False)

    filter_fields = ['departament']
    # permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):

        queryset = Province.objects.filter(is_deleted=False)
        # for field in self.filter_fields:
        #     if field in self.request.GET:
        #         queryset.filter(self.request.GET.get(field))

        if 'departament' in self.request.GET:
            return queryset.filter(departament_id=self.request.GET.get('departament'))

        return queryset


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
        # update Municipaly
        Municipality.objects.filter(Province=instance
                                        ).update(
                                            is_deleted=True,
                                            deleted_at=timezone.now()
                                        )




