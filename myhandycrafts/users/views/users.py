""" User views."""

# Django
from django.utils.translation import ugettext_lazy as _

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import  SearchFilter,OrderingFilter

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response

# Models
from myhandycrafts.users.models import User
from myhandycrafts.users.permissions import IsAdmin,IsAdminorIsOwner

# Serializers
from myhandycrafts.users.serializers import (
    UserModelSerializer,
    UserLoginSerializer,
    UserTemporalPasswordSendSerializer,
    UserUpdatePasswordSerializer,
    UserSignUpSerializer,
    UserProfilePublicSerializer,
    ProfilePictureSerializer,
    ProfileContactSerializer,
    UserUpdateModelSerializer,
    UserShortDetailSerializer,
)

# Pagination
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination

# datetime
from datetime import *



class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """User vies set.
    Handle sing up, log in, and account verification.
    """

    queryset = User.objects.filter(is_deleted=False)
    # serializer_class = UserModelSerializer
    # lookup_field = 'username'
    pagination_class = MyHandycraftsPageNumberPagination

    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('username','created_at')
    ordering_fields = ('username','created_at')
    ordering = ('username','created_at')
    # queryset = Province.objects.filter(is_deleted=False)


    def get_permissions(self):
        """Assing permission based on actions."""
        if self.action in ['login', 'recovery','profilepublic','shortdetail',]:
            permissions = [AllowAny]
        elif self.action in ['register','update','destroy','list']:
            permissions = [IsAuthenticated, IsAdmin]
        elif self.action in ['profilepicture','retrieve','contact','updatepassword']:
            permissions = [IsAuthenticated, IsAdminorIsOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_serializer_class(self):
        """ Assign serializer based on action"""
        if self.action == 'profilepublic':
            return UserProfilePublicSerializer
        if self.action == 'shortdetail':
            return UserShortDetailSerializer
        if self.action == 'update':
            return UserUpdateModelSerializer
        return UserModelSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}


    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'state':1,
            'data':{
                'user': UserModelSerializer(user).data,
                'token': token
            },
            'message':''
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def recovery(self, request):
        serializer = UserTemporalPasswordSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'state': 1,
            'data':'',
            'message':'Your Password has send to your email.'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def updatepassword(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserUpdatePasswordSerializer(
            instance,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'state': 1,
            'data':'',
            'message':'Password has been updated'

        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSignUpSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'state': 1,
            'data': UserModelSerializer(user).data
        }
        return Response(data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'])
    def profilepublic(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def shortdetail(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def profilepicture(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfilePictureSerializer(instance.profile
                                              ,data=request.data
                                              )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'state': 1,
            'data':UserModelSerializer(instance).data,
            'message': _("The user picture was uploaded ")
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def contact(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileContactSerializer(instance.profile,
                                              data=request.data
                                              )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'state': 1,
            'data':UserModelSerializer(instance).data,
            'message': "Contact information was updated"
        }
        return Response(data, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserUpdateModelSerializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserModelSerializer(instance).data)


    def perform_destroy(self, instance):
        instance.is_deleted=True
        instance.deleted_at = datetime.now()
        instance.deleted_by = self.request.user.pk
        instance.save()

