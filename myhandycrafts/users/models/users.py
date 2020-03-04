"""User Model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


#Utilities
from myhandycrafts.utils.models import MyHandycraftsModel

class User(MyHandycraftsModel,AbstractUser):
    """User Model.
    Extends from Django's abstract user, change the
    username field to email and add some extra field.
    """

    email=models.EmailField(
        'email',
        unique=True,
        error_messages={
            'unique':_('A user with  thise email already exists.')
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text=_('Set to true when the user have verified its email address.')
    )

    is_craftsman = models.BooleanField(
        'craftsman',
        default=True,
        help_text=_(
            'User is craftsman. '
            'Clients are the main type of user.'
        )
    )

    TYPE_CHOICES = (
        ('A', 'Admin'),
        ('B', 'Craftsman'),
        ('C', 'Client'),
    )
    type_user = models.CharField(max_length=1, choices=TYPE_CHOICES,default='C')


    def __str__(self):
        """Return firstaname and last name"""
        return "{} {}".format(
            self.first_name,
            self.last_name
        )

    def get_short_name(self):
        """Return username"""
        return self.username
