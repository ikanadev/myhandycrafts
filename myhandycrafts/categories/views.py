"""Category views."""

# Django REST Framework
from rest_framework import mixins,viewsets

# Permisions
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny

# Serilizers
from myhandycrafts.categories.serializers import (
    CategoryModelSerializer,
    CategoryListSerializer,
)



# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend

# Models
from myhandycrafts.categories.models import Category

# Pagination
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination


# time
from django.utils import timezone

class CategoryViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Category view set."""

    serializer_class = CategoryModelSerializer
    pagination_class = MyHandycraftsPageNumberPagination
    # filter name
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name','count_post','count_craftman','created_at',)
    # filter_fields = ('name')

    queryset = Category.objects.filter(active=True)

    def get_permissions(self):
        """Assing permision base on action."""
        permissions = []
        if self.action in ['create','update','destroy']:
            permissions.append(IsAdminUser)
        else:
            permissions.append(AllowAny)
        return [permission() for permission in permissions]

    def perform_destroy(self, instance):
        instance.active=False
        instance.deleted_at = timezone.now()
        instance.save()
        """assing polices"""


class CategoryListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = CategoryListSerializer
    # pagination_class = MyHandycraftsPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name', 'count_post', 'count_craftman', 'created_at',)
    # filter_fields = ('name')

    queryset = Category.objects.filter(active=True)





