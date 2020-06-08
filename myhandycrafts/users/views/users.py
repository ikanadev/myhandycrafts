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
from myhandycrafts.categories.models import Category
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
    UserDetailModelSerializer,
    UserListSerializer,
)

# Pagination
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination

# datetime
from datetime import *

# Utilities
from myhandycrafts.utils.token import get_response_token




class UserAdminViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """User vies set.
    Handle sing up, log in, and account verification.
    """

    queryset = User.objects.filter(active=True)
    pagination_class = MyHandycraftsPageNumberPagination

    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('email',
                     'username',
                     'first_name',
                     'last_name',
                     'profile__ci',
                     )
    ordering_fields = ('email',
                     'username',
                     'first_name',
                     'last_name',
                     'created_at',
                     'category',
                    )

    ordering = ('last_name','created_at')

    permission_classes = [IsAuthenticated,IsAdmin]

    def get_queryset(self):
        queryset = User.objects.filter(active=True)
        if 'category' in self.request.GET:
            try:
                category_id = int(self.request.GET.get('category'))
                category = Category.objects.get(pk = category_id)
                queryset = queryset.filter(profile__category=category)
            except (ValueError,Category.DoesNotExist):
                pass

        return queryset




    def get_serializer_class(self):
        """ Assign serializer based on action"""
        if self.action == 'update':
            return UserUpdateModelSerializer
        if self.action in ['details','list','retrieve']:
            return UserDetailModelSerializer
        return UserModelSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}


    @action(detail=False, methods=['post'])
    def register(self, request):
        """CREATE  USER"""
        serializer = UserSignUpSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data =  UserDetailModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """UPDATE USER"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserUpdateModelSerializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserDetailModelSerializer(instance).data)

    def perform_destroy(self, instance):
        """DELETE"""
        instance.active=False
        instance.deleted_at = datetime.now()
        instance.deleted_by = self.request.user.pk
        instance.save()

    @action(detail=True, methods=['POST'])
    def profilepicture(self, request, *args, **kwargs):
        """update profile picture"""
        instance = self.get_object()
        serializer = ProfilePictureSerializer(instance.profile
                                              ,data=request.data
                                              )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserDetailModelSerializer(instance).data
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
            'data': '',
            'message': 'Password has been updated'

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
        data =  UserDetailModelSerializer(instance).data
        return Response(data, status=status.HTTP_200_OK)



class UserListAdminViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """User list for dropdown

    return a list of users for select dropdown
    """
    # pagination_class = MyHandycraftsPageNumberPagination # =withouth pagination

    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('email',
                     'username',
                     'first_name',
                     'last_name',
                     'profile__ci',
                     )
    ordering_fields = ('email',
                     'username',
                     'first_name',
                     'last_name',
                     'created_at',
                     'category',
                    )

    ordering = ('last_name','created_at')
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = User.objects.filter(active=True,is_staff=False)
        if 'category' in self.request.GET:
            try:
                category_id = int(self.request.GET.get('category'))
                category = Category.objects.get(pk=category_id)
                queryset = queryset.filter(profile__category=category)
            except (ValueError, Category.DoesNotExist):
                pass
        return queryset


class UserUserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """User vies set.
    Handle sing up, log in, and account verification.
    """

    queryset = User.objects.filter(active=True,is_staff=False)
    pagination_class = MyHandycraftsPageNumberPagination

    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('username','created_at')
    ordering_fields = ('username','created_at')
    ordering = ('username','created_at')



    def get_permissions(self):
        """Assing permission based on actions."""
        if self.action in ['login', 'recovery','profilepublic','shortdetail',]:
            permissions = [AllowAny]
        elif self.action in ['register','update','destroy','list',]:
            permissions = [IsAuthenticated, IsAdmin]
        elif self.action in ['profilepicture','retrieve','contact','updatepassword','details']:
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
        if self.action in ['details','list','retrieve']:
            return UserDetailModelSerializer
        return UserModelSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}


    def retrieve(self, request, *args, **kwargs):
        """read"""
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def updatepassword(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = UserUpdatePasswordSerializer(
            instance,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'state': 1,
            'data': '',
            'message': 'Password has been updated'
        }
        return Response(data, status=status.HTTP_200_OK)



    @action(detail=True, methods=['POST'])
    def profilepicture(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = ProfilePictureSerializer(instance.profile
                                              ,data=request.data
                                              )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'state': 1,
            'data':UserDetailModelSerializer(instance).data,
            'message': _("The user picture was uploaded ")
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def contact(self, request, *args, **kwargs):
        instance = self.request.user
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


    @action(detail=False, methods=['post'])
    def credential(self, request):
        """Return credential to user"""
        user = self.request.user
        token = get_response_token(user.pk, False)
        data = {
            'state': 1,
            'data': {
                'user': UserDetailModelSerializer(user).data,
                'token': token
            },
            'message': ''
        }
        return Response(data, status=status.HTTP_200_OK)






class UserClientViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """User vies set.
    Handle sing up, log in, and account verification.
    """

    queryset = User.objects.filter(active=True,is_staff=False)
    pagination_class = MyHandycraftsPageNumberPagination

    filter_backends = (
        SearchFilter,
        OrderingFilter,
        # filters.DjangoFilterBackend
    )
    search_fields = ('email',
                     'username',
                     'first_name',
                     'last_name',
                     'profile__ci',
                     )
    ordering_fields = ('email',
                       'username',
                       'first_name',
                       'last_name',
                       'created_at',
                       'category',
                       )
    ordering = ('last_name', 'created_at')
    permission_classes = [AllowAny]


    def get_serializer_class(self):
        """ Assign serializer based on action"""
        if self.action == 'profilepublic':
            return UserProfilePublicSerializer
        if self.action == 'shortdetail':
            return UserShortDetailSerializer
        return UserModelSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}


    @action(detail=False, methods=['post'])
    def login(self, request):
        """access to system"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'state':1,
            'data':{
                'user': UserDetailModelSerializer(user).data,
                'token': token
            },
            'message':''
        }
        return Response(data, status=status.HTTP_200_OK)



    @action(detail=False, methods=['post'])
    def recovery(self, request):
        """Recovery new password account"""
        serializer = UserTemporalPasswordSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'state': 1,
            'data':'',
            'message':'Your Password has send to your email.'
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
