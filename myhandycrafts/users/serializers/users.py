"""User Serializers."""

# Django
from django.conf import settings
from django.contrib.auth import password_validation,authenticate
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from myhandycrafts.users.models import User,Profile,UserTemporalPassword
from django.utils.translation import ugettext_lazy as _


# Utilities
from myhandycrafts.utils.token import get_response_token

# Utils
import random
import string
import hashlib

from datetime import datetime,timedelta



# Email
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



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
        self.context['reset_password'] = False
        email=data['email']
        password=data['password']
        user=authenticate(username=email,password=password)
        if not user:
            try:
                user = User.objects.get(email=email)
                user_auth = UserTemporalPassword.objects.get(
                    user=user,
                    password=hashlib.sha256(password.encode('utf-8')).hexdigest(),
                    created_at__gte=datetime.now() - timedelta(minutes=60)
                ).user
                self.context['reset_password'] = True
                user.is_active = True
                user.save()
            except (UserTemporalPassword.DoesNotExist, User.DoesNotExist):
                raise serializers.ValidationError('Invalid Credential.')

        if not user.is_verified:
            raise serializers.ValidationError(_('Acount is not active'))




        self.context['user']=user
        return data


    def create(self,data):
        """Generate token login."""
        token = self.get_token()
        return self.context['user'],token


    def get_token(self):
        """Return  response toke. """
        return get_response_token(
            self.context['user'].id,
            self.context['reset_password']
        )


class UserTemporalPasswordSendSerializer(serializers.Serializer):
    """User temporal password send email with temporal password."""
    email = serializers.EmailField()
    def validate_email(self,data):
        """Verify email valid."""
        try:
            user = User.objects.get(email=data)
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not relationated with any account.")
        self.context['user']=user
        return data

    def save(self):
        """Send Mail with temporal password."""
        user = self.context['user']
        password_temporal = self.get_temporar_password()
        UserTemporalPassword.objects.create(
            user=user,
            password=hashlib.sha256(password_temporal.encode('utf-8')).hexdigest()
        )
        self.send_email(password_temporal)

    def get_temporar_password(self):
        """Return password hash"""
        letters = string.ascii_lowercase
        temp = ''.join(random.choice(letters) for i in range(10))
        return  hashlib.md5(temp.encode('utf-8')).hexdigest()[3:7] + "x1"


    def send_email(self,password_temporal):
        """Send email with temporal passoword."""
        user = self.context['user']

        subject = 'Estimado {} {}! has solicitado recuperar tu contraseña'.format(
            user.first_name,
            user.last_name
        )
        from_email = 'My HandyCrafts <noreply@comparteride.com>'
        content = render_to_string(
            'email/user_temporal_password.html',
            {'password': password_temporal, 'user': user}
        )
        print(password_temporal)
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()



class UserUpdatePasswordSerializer(serializers.Serializer):
    """ User update his password."""
    password = serializers.CharField(min_length=6)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_password(self,data):
        return data


    def create(self, data):
        user = data['user']
        new_password = data['password']
        user.set_password(new_password)
        user.save()
        return data





