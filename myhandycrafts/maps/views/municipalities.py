"""Departaments views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Serializer
from myhandycrafts.maps.serializers import MunicipalityModelSerializer

# models
from myhandycrafts.maps.models import Municipality


# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter


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
    # queryset = Municipality.objects.filter(is_deleted=False)

    filter_fields = ['departament','province']
    # permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):
        """ queryset with filter departament, and province"""
        queryset = Municipality.objects.filter(is_deleted=False)
        # for field in self.filter_fields:
        #     if field in self.request.GET:
        #         queryset.filter(self.request.GET.get(field))

        if 'departament' in self.request.GET:
            queryset = queryset.filter(departament_id=self.request.GET.get('departament'))

        if 'province' in self.request.GET:
            queryset = queryset.filter(province_id=self.request.GET.get('province'))

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





