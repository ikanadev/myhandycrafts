"""Categories Model."""

# Django
from django.db import models

# Utilities
from myhandycrafts.utils.models import MyHandycraftsModel


class Category(MyHandycraftsModel):
    """ Category model.

    This model represent the category of craft
    that make the craftsman.
    """

    name = models.CharField(
        'Rubro name',
        max_length=128,
        blank=False,
    )

    description = models.TextField(max_length=512, blank=True)

    #statitics

    count_post = models.PositiveIntegerField(default=0)
    count_craftman = models.PositiveIntegerField(default=0)


    def __str__(self):
        """ Return category name"""
        return self.name
