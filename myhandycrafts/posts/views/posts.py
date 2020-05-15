"""Post view."""
# Django REST Framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# permissions
from rest_framework.permissions import IsAuthenticated,AllowAny

# filters
from rest_framework.filters import SearchFilter,OrderingFilter

# Serializers
from myhandycrafts.posts.serializers import (
    PostModelSerializer,
    PostDetailModelSerializer,
)

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
                       'created_at',
                       )
    ordering = ('title','updated_at')
    # filter_fields = ('user')
    # queryset =  Post.objects.filter(active=True)
    pagination_class = MyHandycraftsPageNumberPagination

    def get_queryset(self):

        user = self.request.user

        q = Post.objects.filter(active=True)

        if not user.is_staff:
            print("aqui")
            q = q.filter(user=user)

        else:
            if 'user' in self.request.GET:
                user_id = self.request.GET.get('user')
                q = q.filter(user_id = user_id)

        if 'category' in self.request.GET:
            category_id = self.request.GET.get('category')
            q = q.filter(category_id = category_id)

        print(q.query)
        return q

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]

        if self.action == 'retrieve':
            permissions = [AllowAny]
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'user':self.request.user}

    def get_serializer_class(self):
        if self.action in ['retrieve','list']:
            return PostDetailModelSerializer
        return PostModelSerializer

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data =  PostDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = PostDetailModelSerializer(instance).data
        return Response(data)



