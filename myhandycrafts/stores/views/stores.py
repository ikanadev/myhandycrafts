"""Store view."""
# Django REST Framework
from rest_framework import viewsets

# permissions
from rest_framework.permissions import IsAuthenticated

# filters
from rest_framework.filters import SearchFilter,OrderingFilter

# Serializers
from myhandycrafts.stores.serializers import StoreModelSerializer

# Models
from myhandycrafts.stores.models import Store

# Django
from django.utils import timezone

#Pagination
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination

class StoreViewSet(viewsets.ModelViewSet):
    """Store view set."""
    serializer_class = StoreModelSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('name','description')
    ordering_fields = ('name',
                       'user',
                       'municipaly',
                       'reputation',
                       'publications',
                       'visits',
                       )
    ordering = ('name','updated_at')
    filter_fields = ('user','municipality')
    queryset =  Store.objects.filter(is_deleted=False)
    pagination_class = MyHandycraftsPageNumberPagination

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'user':self.request.user}

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""
