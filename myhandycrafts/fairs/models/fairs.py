"""Fair model."""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel
from myhandycrafts.utils.image_helper import ImageHelper

# models
from myhandycrafts.users.models import User


class Fair(MyHandycraftsModel):
    """Fair model.

    A fair model represent a fair  for  craftmans, user can publish his
    products, that he want to sell, join to fair.
    On fair user can create relationship between produt's publish
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='creator of fair',
        related_name='fairs'
    )

    municipality = models.ForeignKey(
        'maps.Municipality',
        on_delete=models.SET_NULL,
        null=True,
        help_text='municipality where fair stay',
        related_name='fairs'
    )

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True,max_length=1024)

    ubicacion = models.TextField(max_length=512)
    gps = models.CharField(max_length=10)
    date_init = models.DateField()
    date_end = models.DateField()
    time_init = models.TimeField(null=True)
    time_end = models.TimeField(null=True)

    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='limited fair can grow up a to '
                  'fixed number of participant'
    )
    participant_limit =models.PositiveIntegerField(
        default=0,
        help_text='If the fair is limited, this will be the limit '
                  'on the number of participants'
    )


    # stats
    reputation = models.FloatField(
        default=5.0,
        help_text="Fair's reputation based on crafts."
    )
    publications = models.PositiveIntegerField(default=0)
    visits = models.PositiveIntegerField(default=0)

    class Meta:
        """Class Meta"""
        verbose_name = "Fair"
        verbose_name_plural = "Fairs"

    def __str__(self):
        return  self.name




