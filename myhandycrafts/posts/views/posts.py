"""Post view."""
# Django REST Framework
from rest_framework import viewsets,mixins,status
from rest_framework.response import Response

# permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# filters
from rest_framework.filters import SearchFilter,OrderingFilter

# Serializers
from myhandycrafts.posts.serializers import (
    PostModelSerializer,
    PostDetailModelSerializer,
)

# Models
from myhandycrafts.users.models import User
from myhandycrafts.categories.models import Category
from myhandycrafts.posts.models import Post


# Django
from django.utils import timezone

#Pagination
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination


class PostAdminViewSet(viewsets.ModelViewSet):
    """Post view set."""
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','description')
    ordering_fields = ('title',
                       'visits',
                       'created_at',
                       )
    ordering = ('title','updated_at')
    pagination_class = MyHandycraftsPageNumberPagination

    def get_queryset(self):

        queryset = Post.objects.filter(active=True)
        if 'user' in self.request.GET:
            try:
                user_id = int(self.request.GET.get('user'))
                user = User.objects.get(pk=user_id)
                queryset = queryset.filter(user=user)
            except (ValueError,User.DoesNotExist):
                pass

        if 'category' in self.request.GET:
            try:
                category_id = int(self.request.GET.get('category'))
                category = Category.objects.get(pk=category_id)
                queryset = queryset.filter(category=category)
            except (ValueError, Category.DoesNotExist):
                pass

        return queryset


    def get_serializer_context(self):
        return {'user':self.request.user}

    def get_serializer_class(self):
        if self.action in ['retrieve','list']:
            return PostDetailModelSerializer
        return PostModelSerializer



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

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""


class PostUserViewSet(viewsets.ModelViewSet):
    """Post view set."""
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','description')
    ordering_fields = ('title',
                       'visits',
                       'created_at',
                       )
    ordering = ('title','updated_at')
    pagination_class = MyHandycraftsPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(active=True,user=user)
        if 'category' in self.request.GET:
            try:
                category_id = int(self.request.GET.get('category'))
                category = Category.objects.get(pk=category_id)
                queryset = queryset.filter(category=category)
            except (ValueError, Category.DoesNotExist):
                pass

        return queryset

    def get_serializer_context(self):
        return {'user':self.request.user}

    def get_serializer_class(self):
        if self.action in ['retrieve','list']:
            return PostDetailModelSerializer
        return PostModelSerializer



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

    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""



class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    """Post view set."""
    serializer_class = PostDetailModelSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','description')
    ordering_fields = ('title',
                       'visits',
                       'created_at',
                       )
    ordering = ('title','updated_at')
    pagination_class = MyHandycraftsPageNumberPagination

    def get_queryset(self):

        queryset = Post.objects.filter(active=True)
        if 'user' in self.request.GET:
            try:
                user_id = int(self.request.GET.get('user'))
                user = User.objects.get(pk=user_id)
                queryset = queryset.filter(user=user)
            except (ValueError,User.DoesNotExist):
                pass

        if 'category' in self.request.GET:
            try:
                category_id = int(self.request.GET.get('category'))
                category = Category.objects.get(pk=category_id)
                queryset = queryset.filter(category=category)
            except (ValueError, Category.DoesNotExist):
                pass

        return queryset




