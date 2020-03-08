""" User views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from myhandycrafts.users.permissions import IsAdmin

# Serializers
from myhandycrafts.users.serializers import (
    UserModelSerializer,
    UserLoginSerializer,
    UserTemporalPasswordSendSerializer,
    UserUpdatePasswordSerializer,
    UserSignUpSerializer,
)

# Models
from myhandycrafts.users.models import User




class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User vies set.
    Handle sing up, log in, and account verification.
    """

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assing permission based on actions."""
        if self.action in ['login','recovery']:
            permissions = [AllowAny]
        elif self.action in ['register']:
            permissions = [IsAuthenticated,IsAdmin]
        else:
             permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token,
        }
        return Response(data, status=status.HTTP_200_OK)


    @action(detail=False,methods=['post'])
    def recovery(self, request):
        serializer = UserTemporalPasswordSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'status':1
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False ,methods=['post'])
    def updatepassword(self,request):
        serializer = UserUpdatePasswordSerializer(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data={
            'status':1
        }
        return Response(data,status=status.HTTP_200_OK)

    @action(detail=False,methods=['post'])
    def register(self,request):
        serializer = UserSignUpSerializer(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        user =serializer.save()
        data = {
            'state': 1,
            'data': UserModelSerializer(user).data
        }
        return Response(data, status=status.HTTP_200_OK)

