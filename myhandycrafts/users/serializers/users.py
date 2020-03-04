"""User Serializers."""

# Django
from django.conf import settings
from django.contrib.auth import password_validation,authenticate
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from myhandycrafts.users.models import User,Profile
from django.utils.translation import ugettext_lazy as _

class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""
    # profile=ProfileModelSerializer(read_only=True)

    class Meta:
        model=User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            # 'profile',
        )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=6,max_length=64)

    def validate(self,data):
        user=authenticate(username=data['email'],password=data['password'])
        if not user:
            raise serializers.ValidationError(_('Invalid Credential.'))

        if not user.is_verified:
            raise serializers.ValidationError(_('Acount is not active'))

        self.context['user']=user
        return data


    def create(self,data):
        """Generate token login."""
        token = self.get_token()
        return self.context['user'],token


    def get_token(self):
        return "token"