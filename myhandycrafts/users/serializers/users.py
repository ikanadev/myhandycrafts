"""User Serializers."""

import hashlib
# Utils
import random
import string
from datetime import datetime, timedelta

# Django
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator

# Email
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from myhandycrafts.categories.models import Category
# Models
from myhandycrafts.users.models import User, Profile, UserTemporalPassword
# Serializer
from myhandycrafts.users.serializers.profiles import (
ProfileModelSerializer,
ProfilePublicModelSerializer,
ProfileDetailModelSerializer
)
# Utilities
from myhandycrafts.utils.token import get_response_token








class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile',
            'is_staff',
        )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=64)

    def validate(self, data):
        self.context['reset_password'] = False
        email = data['email']
        password = data['password']
        user = authenticate(username=email, password=password)
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

        self.context['user'] = user
        return data

    def create(self, data):
        """Generate token login."""
        token = self.get_token()
        return self.context['user'], token

    def get_token(self):
        """Return  response toke. """
        return get_response_token(
            self.context['user'].id,
            self.context['reset_password']
        )


class UserTemporalPasswordSendSerializer(serializers.Serializer):
    """User temporal password send email with temporal password."""
    email = serializers.EmailField()

    def validate_email(self, data):
        """Verify email valid."""
        try:
            user = User.objects.get(email=data)
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not relationated with any account.")
        self.context['user'] = user
        return data

    def save(self):
        """Send Mail with temporal password."""
        user = self.context['user']
        password_temporal = self.get_temporal_password()
        UserTemporalPassword.objects.create(
            user=user,
            password=hashlib.sha256(password_temporal.encode('utf-8')).hexdigest()
        )
        self.send_email(password_temporal)

    def get_temporal_password(self):
        """Return password hash"""
        letters = string.ascii_lowercase
        temp = ''.join(random.choice(letters) for i in range(10))
        return hashlib.md5(temp.encode('utf-8')).hexdigest()[3:7] + "x1"

    def send_email(self, password_temporal):
        """Send email with temporal passoword."""
        user = self.context['user']

        subject = 'Estimado {} {}! has solicitado recuperar tu contraseña'.format(
            user.first_name,
            user.last_name
        )
        # from_email = 'My HandyCrafts <noreply@mg.cheapdinamic.xyz>'
        from_email = 'no-reply@mg.cheapdinamic.xyz'
        content = render_to_string(
            'email/user_temporal_password.html',
            {'password': password_temporal, 'user': user}
        )
        print(password_temporal)
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()


# class UserUpdatePasswordSerializer(serializers.Serializer):
#     """ User update his password."""
#     password = serializers.CharField(min_length=6)
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     def validate_password(self, data):
#         return data
#
#     def create(self, data):
#         user = data['user']
#         new_password = data['password']
#         user.set_password(new_password)
#         user.save()
#         return data


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    """ User update his password."""
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ('password',)

    # def validate_password(self, data):
    #     """rule for password"""
    #     return data

    def update(self, instance, data):
        new_password = data['password']
        instance.set_password(new_password)
        instance.save()
        return instance


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle the register for new user.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.filter(active=True))]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.filter(active=True))]
    )

    password = serializers.CharField(min_length=6, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # ## profile ================
    # picture = serializers.ImageField(
    #     'profile picture',
    #     upload_to='users/pictures/',
    #     blank=True,
    #     null=True
    # )
    biography = serializers.CharField(max_length=500, allow_blank=True)

    ci = serializers.CharField(
        max_length=30,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )

    birth_date = serializers.DateField()

    address = serializers.CharField(max_length=256, allow_blank=True)

    # Category
    category = serializers.IntegerField()

    # Company information
    nit = serializers.CharField(max_length=30, allow_blank=True)
    nit_bussiness_name = serializers.CharField(max_length=512, allow_blank=True)
    nit_is_active = serializers.BooleanField(default=False)

    # Contact Information User
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{6,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)
    website = serializers.CharField(max_length=128, allow_blank=True)
    has_wattsapp = serializers.BooleanField()
    has_facebook = serializers.BooleanField()
    addres_facebook = serializers.CharField(max_length=512, allow_blank=True)

    # stats
    # reputation = serializers.FloatField(
    #     default=5.0,
    #     help_text="User's reputation based on crafts."
    # )
    # publications = models.PositiveIntegerField(default=0)
    # requests = models.PositiveIntegerField(default=0)
    # stores = models.PositiveIntegerField(default=0)
    # participation_in_fairs = models.PositiveIntegerField(default=0)

    def validate_category(self, data):
        try:
            category = Category.objects.get(pk=data)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category not valid')
        self.context['category'] = category
        return data

    def create(self, data):
        creator_user_id = self.context['request'].user.pk
        user = User.objects.create(
            email=data['email'],
            username=data['username'],
            password=make_password(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name'],
            type_user='B',
            is_verified=True,
            is_active=True,
            is_craftsman=True,
            created_by=creator_user_id,
            is_staff=False
        )

        data.pop('email')
        data.pop('username')
        data.pop('password')
        data.pop('first_name')
        data.pop('last_name')
        data.pop('category')

        Profile.objects.create(
            **data,
            user=user,
            category=self.context['category'],
            created_by=creator_user_id
        )
        self.send_activation_account(user)
        return user

    def send_activation_account(self, user):
        print('sending email activation account')
        pass



class UserProfilePublicSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfilePublicModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile',
        )


class UserUpdateModelSerializer(serializers.Serializer):
    """User Update model serializer.
    Handle the register for new user.
    """

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    biography = serializers.CharField(max_length=500, allow_blank=True)

    ci = serializers.CharField(
        max_length=30,
    )

    birth_date = serializers.DateField()

    address = serializers.CharField(max_length=256, allow_blank=True)

    # Category
    category = serializers.IntegerField()

    # Company information
    nit = serializers.CharField(max_length=30, allow_blank=True)
    nit_bussiness_name = serializers.CharField(max_length=512, allow_blank=True)
    nit_is_active = serializers.BooleanField(default=False)

    # Contact Information User
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{6,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)
    website = serializers.CharField(max_length=128, allow_blank=True)
    has_wattsapp = serializers.BooleanField()
    has_facebook = serializers.BooleanField()
    addres_facebook = serializers.CharField(max_length=512, allow_blank=True)


    def validate_category(self, data):
        try:
            category = Category.objects.get(pk=data)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category not valid')
        self.context['category'] = category
        return data

    def update(self, instance, data):
        user_attr =['first_name','last_name',]
        profile_attr=[
            "biography",
            "ci",
            "birth_date",
            "address",
            "nit",
            "nit_bussiness_name",
            "phone_number",
            "website",
            "has_wattsapp",
            "has_facebook",
            "addres_facebook",
            ]

        profile = instance.profile

        for attr, value in data.items():
            if attr in user_attr:
                setattr(instance, attr, value)
            elif attr in profile_attr:
                setattr(profile, attr, value)

        instance.save()
        profile.save()

        return self.instance



class UserShortDetailSerializer(serializers.ModelSerializer):
    """User model serializer."""

    picture = serializers.SerializerMethodField()

    def get_picture(self,obj):
        return ProfileModelSerializer(obj.profile).data['picture']


    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'picture',
        )



class UserDetailModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileDetailModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile',
            'is_staff',
        )