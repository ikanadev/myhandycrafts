"""Post view."""
# Django REST Framework
from rest_framework import viewsets

# permissions
from rest_framework.permissions import IsAuthenticated

# filters
from rest_framework.filters import SearchFilter,OrderingFilter

# Serializers
from myhandycrafts.posts.serializers import PostModelSerializer

# Models
from myhandycrafts.posts.models import Post

# Django
from django.utils import timezone

#Pagination
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination

class PostViewSet(viewsets.ModelViewSet):
    """Post view set."""
    serializer_class = PostModelSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','description')
    ordering_fields = ('title',
                       'visits',
                       )
    ordering = ('title','updated_at')
    # filter_fields = ('user')
    queryset =  Post.objects.filter(is_deleted=False)
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
