"""Store model."""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel

# Postgress
from django.contrib.postgres.fields import JSONField


class Store(MyHandycraftsModel):
    """Store model.

    A store model represent a store of a craftman, user can publish his
    products, that he want to sell.
    On store user can create relationship between produt's publish and store
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='User is property of store',
        related_name='stores'
    )

    municipality = models.ForeignKey(
        'maps.Municipality',
        on_delete=models.SET_NULL,
        null=True,
        help_text='municipality where store stay',
        related_name='stores'
    )

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True,max_length=1024)

    location = models.TextField(max_length=512)
    gps = JSONField(null=True)

    # stats
    reputation = models.FloatField(
        default=5.0,
        help_text="Store's reputation based on crafts."
    )
    publications = models.PositiveIntegerField(default=0)
    visits = models.PositiveIntegerField(default=0)

    class Meta:
        """Class Meta"""
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return  self.name



