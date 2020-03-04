"""User Model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

#Utilities
from myhandycrafts.utils.models import MyHandycraftsModel

class TemporalUser(MyHandycraftsModel):
    """Temporal User Model.
    Temporal user is an object that make requests and reservations.
    """
    name=models.CharField(
        'name',
        max_length=256,
        blank=False,
        help_text=_('Temporal user name')
    )

    email=models.EmailField(
        'email',
        unique=True,
        error_messages={
            'unique':_('A user with  thise email already exists.')
        }
    )

    code_devide=models.CharField(max_length=516,blank=True)

    # Contact Information User
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{6,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text=_('Set to true when the user have verified its email address.')
    )


    def __str__(self):
        """ Return name and email"""
        return "{} {}".format(
            self.name,
            self.email
        )